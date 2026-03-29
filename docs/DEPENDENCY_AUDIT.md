# Dependency audit (Python / PyPI)

**CI** runs **PyPA [pip-audit](https://pypi.org/project/pip-audit/)** on the **editable** install graph after
**`pip install -e ".[dev]"`**. This is the **single** documented playbook for **Python** supply-chain advisories;
**browser** / **npm** surfaces are separate — see **[`docs/FRONTEND_SUPPLY_CHAIN.md`](FRONTEND_SUPPLY_CHAIN.md)** (**A3**).

Normative **CI** contract: **[`docs/DESIGN_PRINCIPLES.md` — GitHub Actions CI workflow](DESIGN_PRINCIPLES.md#github-actions-ci-workflow)**
(**Supply chain** row). The **`supply-chain`** job in **`.github/workflows/ci.yml`** MUST stay aligned with this file
(**`pip-audit`** CLI flags and every **`--ignore-vuln`** ID).

---

## What CI runs today

After **`pip install -e ".[dev]"`** on **Python 3.12** (**`ubuntu-latest`**), the workflow runs:

```bash
pip-audit --ignore-vuln CVE-2026-4539 --desc
```

- **`--desc`** prints short descriptions in logs (helps triage without opening every advisory URL).
- **PyPA pip-audit** does **not** support a **`--severity-high`**-style filter; **any** reported vulnerability fails the
  job **unless** it is remediated (bump/pin) **or** explicitly ignored here and in **`.github/workflows/ci.yml`**.
- **`--ignore-vuln`** is **not** a silent bypass: each ID MUST have a matching subsection under
[**Documented vulnerability overrides**](#documented-vulnerability-overrides) below.

---

## Reproduce locally

Use the same install graph **CI** audits (editable package + **dev** extras):

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
pip-audit --ignore-vuln CVE-2026-4539 --desc
```

To see what **CI** would fail on **without** repo-approved ignores (useful before opening a PR):

```bash
pip-audit --desc
```

If **`pip-audit`** is missing, ensure **`pip install -e ".[dev]"`** succeeded — **`pip-audit`** is listed under
**`[project.optional-dependencies].dev`** in **`pyproject.toml`**.

---

## Reading a failure

Typical **`pip-audit`** output names:

- **Distribution** (PyPI name) and **installed version** on your graph.
- **CVE** or advisory ID and (when known) a **fixed** version range.

**Order of operations for contributors:**

1. **Confirm** you reproduced with the commands above (same flags as **CI** when testing the merge gate).
2. **Identify** whether the vulnerable package is a **direct** dependency in **`pyproject.toml`** (**`[project].dependencies`**
   or **`[project.optional-dependencies].dev`**) or **transitive** (pulled in by something else).
3. **Check** whether a **safe** upgrade exists inside this repo’s **PEP 508** constraints ([**Dependency pins and dev toolchain**](DESIGN_PRINCIPLES.md#dependency-pins-and-dev-toolchain)).

---

## Fix paths: bump, pin, upstream, or override

### Prefer version resolution (bump or constrain)

- **Direct dependency** with a known fix: bump the **PEP 508** line in **`pyproject.toml`** (and **`[build-system].requires`**
  if applicable), then update **[`docs/DESIGN_PRINCIPLES.md`](DESIGN_PRINCIPLES.md)** matrices or pin tables if your
  change moves supported ranges. Record **CHANGELOG** **Unreleased** per **[`CONTRIBUTING.md`](../CONTRIBUTING.md)**.
- **Transitive** dependency: prefer **`pip install -e ".[dev]"`** then inspect **`pip show <dist>`** / dependency tree
  tools to see **who** pulls it in. If a **newer** parent release drops the bad version **without** violating our
  ranges, bump the parent.

### Upstream issue vs pinning in this repo

| Situation | Preferred action |
| --------- | ---------------- |
| Fix exists upstream but not yet in a release we can use | Open or follow an **issue** on the **maintainer** package (or security tracker); link it from the PR **or** a short note in **CHANGELOG** if you’re temporarily pinning. |
| No fix yet; we can **exclude** a bad transitive version with a **direct** constraint | Add a **PEP 508** constraint in **`pyproject.toml`** **only** with maintainer review — document **why** in **CHANGELOG** **Unreleased** and keep [**DESIGN_PRINCIPLES**](DESIGN_PRINCIPLES.md) / [**compat**](compat.md) wording honest. |
| Noise / **accepted risk** with written rationale | Use **`--ignore-vuln`** **only** after filling [**Documented vulnerability overrides**](#documented-vulnerability-overrides) and mirroring the flag in **`.github/workflows/ci.yml`**. |

**Do not** weaken the gate by dropping **`pip-audit`** from **CI** or piping it through **`|| true`** without an explicit
maintainer decision recorded in **CHANGELOG** and **DESIGN_PRINCIPLES**.

### When overrides (`--ignore-vuln`) are acceptable

Overrides are for **documented** exceptions, not routine cleanup:

- The vulnerability is **not exploitable** in this repo’s **usage** (support with a short technical reason — e.g. unused
  code path, CLI-only vs web attack surface).
- A fix is **in flight** and the ignore is **time-bounded** in prose (“revisit on next **replayt** / **dev** bump”).
- The advisory is a **false positive** for our context **and** that reasoning is recorded.

Every ignore MUST list **CVE ID**, **rationale**, and **revisit / removal** criteria in this file **before** it appears
in **CI**.

---

## Documented vulnerability overrides

Keep this list in **sync** with **`.github/workflows/ci.yml`** (**`pip-audit`** step). When adding or removing an ignore,
update **both** in one change set and add **CHANGELOG** **Unreleased**.

### CVE-2026-4539 (pygments)

- **Scope:** Transitive **pygments** (often via **rich** / **typer** / dev tooling). **CVE-2026-4539** concerns **ReDoS**
  in **AdlLexer**; this showcase does **not** use that lexer for any supported workflow.
- **Rationale:** Accepted risk until dependency bumps clear the advisory without breaking **[dev]** pins.
- **Removal:** Drop **`--ignore-vuln CVE-2026-4539`** from **CI** and this section when **`pip-audit`** is clean without it.

---

## Acceptance criteria (backlog — documentation)

The backlog **Document pip-audit failures and dependency override playbook** is satisfied when:

| # | Criterion |
| - | --------- |
| **D1** | **`docs/DEPENDENCY_AUDIT.md`** exists and states that **CI** **`supply-chain`** audits the **editable** **`".[dev]"`** graph with **`pip-audit`**. |
| **D2** | The doc quotes or unambiguously references the **same** **`pip-audit`** invocation as **`.github/workflows/ci.yml`** (including **`--ignore-vuln`** flags). |
| **D3** | The doc gives **copy-paste** local steps (**venv**, **`pip install -e ".[dev]"`**, **`pip-audit`** with the **CI-equivalent** flags) plus optional “no ignores” command for triage. |
| **D4** | The doc explains how to **read** a typical failure (package, advisory ID, fixed version when present) and confirms matching the **CI** install graph. |
| **D5** | The doc describes **fix paths**: prefer **version bumps** in **`pyproject.toml`**; **transitive** issues via parent bumps or documented pins; distinguishes **runtime** vs **dev** dependencies at a high level. |
| **D6** | The doc gives **upstream vs pin** guidance (file/track upstream for transitive gaps; **PEP 508** pins only with review + **CHANGELOG**). |
| **D7** | The doc defines when **`--ignore-vuln`** is acceptable and requires each ignored **CVE** to appear under [**Documented vulnerability overrides**](#documented-vulnerability-overrides) **and** in **`.github/workflows/ci.yml`**. |
| **D8** | **Cross-links:** points to **[`docs/FRONTEND_SUPPLY_CHAIN.md`](FRONTEND_SUPPLY_CHAIN.md)** for **JS** / **npm** scope; **[`docs/DESIGN_PRINCIPLES.md`](DESIGN_PRINCIPLES.md)** for the **CI** contract; maintainers keep **[`docs/compat.md`](compat.md)** **EX-SUPPLY-CHAIN** wording consistent when the job changes. |
| **D9** | **`README.md`** includes a **Troubleshooting** (or equivalent) entry that links here for **`pip-audit` / supply-chain** failures. |
| **D10** | Material changes to this playbook or **CI** ignore list include **CHANGELOG** **Unreleased** per project policy. |

**Automated checks (follow-up):** No contract module enforces **D1–D10** in **CI** today. A later phase MAY add
**`tests/test_dependency_audit_doc.py`** (mirroring **`tests/test_frontend_supply_chain_doc.py`**) to assert headings,
keywords, **README** / **DESIGN_PRINCIPLES** links, and **CHANGELOG** mentions.

**Explicit non-goals (this backlog):** Replace **pip-audit** with a different scanner in **CI**; audit **npm** packages
in default **CI**; document **GitHub Dependabot** configuration (unless a separate backlog adds it).
