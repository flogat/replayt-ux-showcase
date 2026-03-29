/*
  P-06 — replayt browser symbols this module calls (check replayt release notes for your CDN pin):
    - window.replayt.player.init({ container, data, theme })
    - Seek (optional, try-order): controller.seekToMs(ms), controller.goto(ms),
      window.replayt.player.seekToMs(ms), window.replayt.player.goto(ms)
      where controller is the return value of init when present.

  Event ordering (P-03): replayt does not document one ordering guarantee for sessionData.events across
  all minors in this repo’s supported range. This demo sorts event times once before computing the scrub range.

  Throttling (P-03): scrub input is coalesced with requestAnimationFrame (at most one seek per frame while dragging).
  change and pointerup run a final applySeekMs so the committed thumb matches the player.

  Tab order (handoff): the range input comes before the player container in DOM order so keyboard users reach
  the scrub control before embedded player focusables. Checklist: ../../a11y/keyboard-model.md
*/

import { useCallback, useEffect, useRef, useState } from "react";

const START_TS = 1704067200000;

/** Same sessionData root shape as docs/examples/basic-player.html and P-03 (fixed literals for copy-paste). */
const SESSION_DATA = {
  events: [
    { timestamp: START_TS + 2000, type: "custom", label: "first paint" },
    { timestamp: START_TS + 45000, type: "custom", label: "mid session" },
    { timestamp: START_TS + 120000, type: "custom", label: "late event" },
    { timestamp: START_TS + 8000, type: "custom", label: "out-of-order in source" },
  ],
  metadata: {
    startTs: START_TS,
    durationMs: 180000,
    viewport: { width: 1920, height: 1080 },
  },
};

function extractEventTimeMs(ev) {
  if (!ev || typeof ev !== "object") return null;
  const raw = ev.timestamp ?? ev.time ?? ev.ts;
  return typeof raw === "number" && !Number.isNaN(raw) ? raw : null;
}

function sortedEventTimes(events) {
  const times = [];
  for (const ev of events) {
    const t = extractEventTimeMs(ev);
    if (t !== null) times.push(t);
  }
  times.sort((a, b) => a - b);
  return times;
}

function computeRangeMs(data) {
  const meta = data.metadata || {};
  const start = typeof meta.startTs === "number" ? meta.startTs : null;
  const dur = typeof meta.durationMs === "number" ? meta.durationMs : null;
  const evTimes = sortedEventTimes(data.events || []);
  const candidates = [];
  if (start !== null) candidates.push(start);
  if (start !== null && dur !== null) candidates.push(start + dur);
  for (const t of evTimes) candidates.push(t);
  if (!candidates.length) return null;
  const minT = Math.min.apply(null, candidates);
  const maxT = Math.max.apply(null, candidates);
  if (minT === maxT) return { minMs: minT, maxMs: minT + 1 };
  return { minMs: minT, maxMs: maxT };
}

function formatClock(ms) {
  const s = Math.max(0, Math.floor(ms / 1000));
  const m = Math.floor(s / 60);
  const r = s % 60;
  return `${m}:${String(r).padStart(2, "0")}`;
}

function pickSeekSink(controller, playerNs) {
  if (controller && typeof controller.seekToMs === "function") {
    return (ms) => controller.seekToMs(ms);
  }
  if (controller && typeof controller.goto === "function") {
    return (ms) => controller.goto(ms);
  }
  if (playerNs && typeof playerNs.seekToMs === "function") {
    return (ms) => playerNs.seekToMs(ms);
  }
  if (playerNs && typeof playerNs.goto === "function") {
    return (ms) => playerNs.goto(ms);
  }
  return null;
}

export default function App() {
  const playerHostRef = useRef(null);
  const scrubberRef = useRef(null);
  const seekSinkRef = useRef(null);
  const rangeInfoRef = useRef(null);
  const rafIdRef = useRef(null);
  const pendingMsRef = useRef(null);

  const [status, setStatus] = useState("Initializing…");
  const [statusError, setStatusError] = useState(false);
  const [readout, setReadout] = useState("—");
  const [scrubDisabled, setScrubDisabled] = useState(true);

  const applySeekMs = useCallback((ms) => {
    const sink = seekSinkRef.current;
    const rangeInfo = rangeInfoRef.current;
    if (!sink || rangeInfo === null) return;
    const clamped = Math.min(rangeInfo.maxMs, Math.max(rangeInfo.minMs, ms));
    sink(clamped);
  }, []);

  const updateReadout = useCallback((ms) => {
    const rangeInfo = rangeInfoRef.current;
    const el = scrubberRef.current;
    if (rangeInfo === null || !el) {
      setReadout("—");
      el?.removeAttribute("aria-valuetext");
      return;
    }
    setReadout(
      `${formatClock(ms)} / ${formatClock(rangeInfo.minMs)}–${formatClock(rangeInfo.maxMs)}`,
    );
    el.setAttribute("aria-valuetext", formatClock(ms));
  }, []);

  const syncAriaValue = useCallback((ms) => {
    const rangeInfo = rangeInfoRef.current;
    const el = scrubberRef.current;
    if (rangeInfo === null || !el) return;
    const span = rangeInfo.maxMs - rangeInfo.minMs;
    const ratio = span > 0 ? (ms - rangeInfo.minMs) / span : 0;
    const stepped = Math.round(ratio * 1000);
    el.setAttribute("aria-valuenow", String(stepped));
  }, []);

  const onScrubInput = useCallback(() => {
    const rangeInfo = rangeInfoRef.current;
    const el = scrubberRef.current;
    if (rangeInfo === null || !el || el.disabled) return;
    const span = rangeInfo.maxMs - rangeInfo.minMs;
    const ratio = Number(el.value) / 1000;
    const ms = rangeInfo.minMs + ratio * span;
    pendingMsRef.current = ms;
    if (rafIdRef.current !== null) cancelAnimationFrame(rafIdRef.current);
    rafIdRef.current = requestAnimationFrame(() => {
      rafIdRef.current = null;
      const v = pendingMsRef.current;
      pendingMsRef.current = null;
      if (v === null) return;
      updateReadout(v);
      syncAriaValue(v);
      applySeekMs(v);
    });
  }, [applySeekMs, syncAriaValue, updateReadout]);

  const onScrubCommit = useCallback(() => {
    const rangeInfo = rangeInfoRef.current;
    const el = scrubberRef.current;
    if (rangeInfo === null || !el || el.disabled) return;
    if (rafIdRef.current !== null) {
      cancelAnimationFrame(rafIdRef.current);
      rafIdRef.current = null;
    }
    pendingMsRef.current = null;
    const span = rangeInfo.maxMs - rangeInfo.minMs;
    const ratio = Number(el.value) / 1000;
    const ms = rangeInfo.minMs + ratio * span;
    updateReadout(ms);
    syncAriaValue(ms);
    applySeekMs(ms);
  }, [applySeekMs, syncAriaValue, updateReadout]);

  useEffect(() => {
    const playerEl = playerHostRef.current;
    const scrubber = scrubberRef.current;
    if (!playerEl || !scrubber) return undefined;

    function setBanner(msg, isError) {
      setStatus(msg);
      setStatusError(isError);
    }

    const rangeInfo = computeRangeMs(SESSION_DATA);
    rangeInfoRef.current = rangeInfo;
    const events = SESSION_DATA.events || [];

    seekSinkRef.current = null;

    if (!events.length) {
      setBanner(
        "No events in sessionData; add events from your replayt API to use the scrubber.",
        true,
      );
      setScrubDisabled(true);
      playerEl.replaceChildren();
      const ph = document.createElement("p");
      ph.style.cssText =
        "display:flex;align-items:center;justify-content:center;height:100%;margin:0;color:#555;text-align:center;padding:1rem;";
      ph.textContent = "Player not initialized (empty timeline).";
      playerEl.appendChild(ph);
      return undefined;
    }

    if (!rangeInfo) {
      setBanner("Could not derive a time range from events and metadata.", true);
      setScrubDisabled(true);
      return undefined;
    }

    scrubber.min = "0";
    scrubber.max = "1000";
    scrubber.value = "0";
    scrubber.setAttribute("aria-valuemin", "0");
    scrubber.setAttribute("aria-valuemax", "1000");
    scrubber.setAttribute("aria-valuenow", "0");
    setScrubDisabled(false);
    updateReadout(rangeInfo.minMs);
    syncAriaValue(rangeInfo.minMs);

    const rtPlayer = window.replayt && window.replayt.player;
    if (!rtPlayer || typeof rtPlayer.init !== "function") {
      setBanner("replayt player not available (check script URL or CDN build).", true);
      playerEl.replaceChildren();
      const ph = document.createElement("p");
      ph.style.cssText =
        "display:flex;align-items:center;justify-content:center;height:100%;margin:0;color:#555;text-align:center;padding:1rem;";
      ph.textContent = "replayt player not loaded.";
      playerEl.appendChild(ph);
      return undefined;
    }

    playerEl.replaceChildren();
    let controller = null;
    try {
      controller = rtPlayer.init({
        container: playerEl,
        data: SESSION_DATA,
        theme: "light",
      });
    } catch {
      setBanner("Player init failed (see console).", true);
      const ph = document.createElement("p");
      ph.style.cssText =
        "display:flex;align-items:center;justify-content:center;height:100%;margin:0;color:#555;text-align:center;padding:1rem;";
      ph.textContent = "Init error.";
      playerEl.appendChild(ph);
      return undefined;
    }

    const sink = pickSeekSink(controller, rtPlayer);
    seekSinkRef.current = sink;
    if (!sink) {
      setBanner(
        "Player loaded, but no published seek hook matched (seekToMs / goto). See Limitations below.",
        true,
      );
    } else {
      setBanner(
        "Scrub to seek; Tab to the slider, then arrow keys. Pointer drag uses rAF-throttled seeks.",
        false,
      );
    }

    applySeekMs(rangeInfo.minMs);

    scrubber.addEventListener("input", onScrubInput);
    scrubber.addEventListener("change", onScrubCommit);
    scrubber.addEventListener("pointerup", onScrubCommit);

    return () => {
      scrubber.removeEventListener("input", onScrubInput);
      scrubber.removeEventListener("change", onScrubCommit);
      scrubber.removeEventListener("pointerup", onScrubCommit);
      if (rafIdRef.current !== null) cancelAnimationFrame(rafIdRef.current);
      rafIdRef.current = null;
      pendingMsRef.current = null;
      seekSinkRef.current = null;
      rangeInfoRef.current = null;
      playerEl.replaceChildren();
      setScrubDisabled(true);
    };
  }, [applySeekMs, onScrubCommit, onScrubInput, syncAriaValue, updateReadout]);

  return (
    <div
      style={{
        fontFamily: "system-ui, sans-serif",
        maxWidth: "1200px",
        margin: "0 auto",
        padding: "2rem",
        color: "#222",
      }}
    >
      <h1>Timeline scrubber + player (P-06, React)</h1>
      <div
        style={{
          background: "#f4f4f5",
          padding: "1rem",
          borderRadius: "8px",
          marginBottom: "1rem",
          border: "1px solid #e0e0e0",
        }}
      >
        <p style={{ margin: 0 }}>
          <strong>P-06:</strong> Same <code>sessionData</code> root and{" "}
          <code>replayt.player.init</code> contract as{" "}
          <a href="../basic-player.html">basic-player.html</a>; scrub UX follows{" "}
          <a href="../timeline-scrubber.html">timeline-scrubber.html</a> (P-03). Keyboard / focus:{" "}
          <a href="../../a11y/keyboard-model.md">docs/a11y/keyboard-model.md</a>.
        </p>
      </div>
      <p
        role="status"
        aria-live="polite"
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          minHeight: "2.5rem",
          margin: "0 0 0.75rem",
          color: statusError ? "#b42318" : "#555",
          fontWeight: statusError ? 600 : 400,
        }}
      >
        {status}
      </p>
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          alignItems: "center",
          gap: "0.75rem",
          margin: "0.75rem 0 1rem",
          padding: "0.5rem 0.75rem",
          border: "1px solid #e0e0e0",
          borderRadius: "8px",
          background: "#fff",
        }}
      >
        <label
          htmlFor="timeline-scrubber-react"
          style={{ fontWeight: 600, minWidth: "7rem" }}
        >
          Session timeline
        </label>
        <input
          ref={scrubberRef}
          type="range"
          id="timeline-scrubber-react"
          min={0}
          max={1000}
          defaultValue={0}
          disabled={scrubDisabled}
          aria-label="Session timeline scrubber"
          style={{
            flex: "1 1 200px",
            minWidth: "160px",
            accentColor: "#007bff",
          }}
        />
        <span
          aria-hidden="true"
          style={{ fontVariantNumeric: "tabular-nums", minWidth: "12rem" }}
        >
          {readout}
        </span>
      </div>
      <div
        ref={playerHostRef}
        style={{
          width: "100%",
          height: "55vh",
          border: "1px solid #e0e0e0",
          borderRadius: "8px",
        }}
      />
      <section
        style={{
          marginTop: "1.25rem",
          padding: "0.75rem 1rem",
          borderLeft: "4px solid #e0e0e0",
          background: "#f4f4f5",
          fontSize: "0.9rem",
        }}
        aria-labelledby="p06-limitations-heading"
      >
        <h2 id="p06-limitations-heading" style={{ margin: "0 0 0.35rem", fontSize: "1rem" }}>
          Limitations
        </h2>
        <p style={{ margin: 0 }}>
          Some CDN builds omit or rename seek and event APIs. Pin a replayt version whose browser bundle matches the
          symbols in the header comment above; upgrade if <code>init</code> works but seek hooks are missing.
        </p>
      </section>
    </div>
  );
}
