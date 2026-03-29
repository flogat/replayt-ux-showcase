# Bundled upstream reference documentation (optional)

This directory is **optional**. A default clone may contain **only** this **`README.md`** so integrators and **CI** stay lean; maintainers, **Mission Control**, and contributors can add **markdown** snapshots here when offline or agent context should mirror a specific **replayt** release.

**Authority:** The **replayt** package on **PyPI**, its published release notes, and upstream project docs remain **canonical**. Content here is a **convenience copy**, not a fork or substitute.

## Goals

- Give humans and automation **stable, grep-friendly** context aligned with the **replayt** versions this repo supports (see **`pyproject.toml`** and **[`docs/DESIGN_PRINCIPLES.md`](../DESIGN_PRINCIPLES.md#replayt-and-python-matrix)**).
- Avoid **bloating** default checkouts: prefer **small**, **text-first** trees; do not require snapshots for **`pytest`** or integrator workflows.

## Layout (normative for maintainers)

Place material under a **clear provenance root**, for example:

| Path (example) | Purpose |
| ---------------- | ------- |
| `docs/reference-documentation/replayt/` | Upstream **replayt**-project markdown (or generated docs exported as **`.md`**) |
| `docs/reference-documentation/replayt/<version>/` | Optional per-version folder when multiple pins need side-by-side context (e.g. **`0.4.25`**) |

**File naming:** Keep upstream-relative paths where practical (e.g. `docs/…` → `replayt/docs/…`) so diffs are reviewable.

## License and attribution

Before committing any snapshot:

1. **Confirm redistribution** is allowed under **replayt**’s license and your source (release tarball, **Git** checkout, doc export).
2. Add or preserve **copyright and license** notices:
   - Prefer a **`LICENSE`** or **`NOTICE`** file beside the snapshot tree **or**
   - A short **`PROVENANCE.md`** at the snapshot root listing **source URL**, **commit** or **tag**, **replayt** **PyPI** version (if applicable), **copy date**, and **license** name with a pointer to the upstream **`LICENSE`** text.
3. Do **not** commit credentials, environment files, or unpublished third-party material.

## Refresh cadence (recommended)

| Trigger | Action |
| ------- | ------ |
| **Showcase** bumps the supported **replayt** range or **CI** reference pin | Refresh or **verify** snapshots still match the documented upstream release; update **`PROVENANCE.md`** (or equivalent) in the **same** maintenance pass as pin/docs updates when snapshots are committed. |
| **Scheduled** hygiene | At least **quarterly**, or before a **minor**/**major** showcase release, spot-check that linked upstream paths still exist. |
| **Mission Control** / release prep | Use the [maintenance checklist](#maintenance-checklist-contributors--mission-control) below when refreshing agent context. |

**CHANGELOG:** When committed snapshots materially change (add/remove/update bulk upstream docs), add a **`[Unreleased]`** note per **[`CONTRIBUTING.md`](../../CONTRIBUTING.md)**.

## Optional automation (Builder phase)

Implementation is **optional**. If maintainers add a helper, it SHOULD:

- Live under **`scripts/`** (for example **`scripts/refresh-reference-docs/`**), **not** under **`src/replayt_ux_showcase/`**.
- Be **documented** in this **`README`** (inputs, outputs, idempotency, required tools).
- **Not** run in default **CI** jobs unless a future backlog explicitly adds a contract; default **pytest** must remain usable without upstream checkouts.

## Maintenance checklist (contributors / Mission Control)

Use this when refreshing bundled context:

- [ ] Identify **source**: upstream **tag**/**commit** or **PyPI** sdist/wheel docs path.
- [ ] Confirm **license** allows redistribution and record it in **`PROVENANCE.md`** (or upstream **`LICENSE`** copy).
- [ ] Copy **markdown** (or lightweight text) only unless a maintainer explicitly approved other formats for size/legal reasons.
- [ ] Align with **[`pyproject.toml`](../../pyproject.toml)** **replayt** constraint (snapshot should not advertise unsupported APIs for integrators without an exempt note in **DESIGN_PRINCIPLES**).
- [ ] Update **`PROVENANCE.md`** **version** and **date** fields.
- [ ] If the change is substantive, add **`CHANGELOG.md`** **`[Unreleased]`** bullet (see **[`CONTRIBUTING.md`](../../CONTRIBUTING.md)**).

## Acceptance criteria (Builder / gate)

The following are **done** when this backlog is implemented:

1. **`docs/reference-documentation/README.md`** (this file) is present and linked from the root **[`README.md`](../../README.md)** and **[`CONTRIBUTING.md`](../../CONTRIBUTING.md)**.
2. **License / provenance** rules above are satisfied for any **committed** snapshot under this tree.
3. **Layout** follows the **path** conventions (or the **README** documents a deliberate, reviewed exception).
4. **Refresh** expectations (**triggers** + checklist) are followed for maintenance; **CHANGELOG** updated when snapshot content changes.
5. Any **optional script** under **`scripts/`** is documented here and is **not** required for **`pip install -e ".[dev]"`** + **`pytest`**.

Further normative cross-links: **[`docs/DESIGN_PRINCIPLES.md` — Backlog traceability: Bundled upstream reference docs workflow](../DESIGN_PRINCIPLES.md#backlog-traceability-bundled-upstream-reference-docs-workflow)**.
