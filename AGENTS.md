# KubeBlocks Skills Maintainer Guide

This file is for **AI maintainers who modify this repository**.

Use the top-level documents like this:

- `README.md`: public guide for human readers and cold-start agents that consume the installed repo.
- `AGENTS.md`: maintainer contract for AI agents who change repo structure, truth files, skills, tests, or validation behavior.
- `SKILL.md`: router-only entrypoint for runtime use. It should choose the next hop, not explain repo maintenance.

If you are changing the repo, read this file first.

## Repository Goal

This repository exists for one outcome:

**a cold-start agent should behave like a practical KubeBlocks operator without guessing and without needing private maintainer context.**

That means:

- the main runtime path must work from **this repo + official public KubeBlocks docs + cluster access**
- a stronger agent may inspect `kubeblocks-addons` or KubeBlocks core repos, but that is optional secondary evidence
- addon/core repos must never become the required runtime prerequisite for the main path
- if a create, ops, observability, or troubleshoot flow still requires raw upstream repo inspection to proceed safely, treat that as a repo defect and fix the repo here

## Non-Negotiable Invariants

These rules are hard constraints. Do not violate them unless the repo is being intentionally re-architected.

### Layout

- `skills/` contains executable skills only, including compatibility shims.
- Top-level directories outside `skills/` are for facts, schemas, references, templates, tests, and scripts.
- Do not create real executable skills under top-level logical folders such as `router/`, `profiles/`, `engines/`, `ops/`, or `observability/`.

### Routing Model

- Mainline stays: `router -> environment gate -> dedicated engine | generic fallback -> capability layers -> observability -> troubleshoot/recovery`.
- `family` is reference-only taxonomy. It is not a cold-start create-time primary entry.
- Tier-1 dedicated engines must not route back to generic, family, or legacy addon entry skills.
- Unknown rollout readiness means `kubeblocks-preflight` comes before first-time provisioning.

### Truth Model

- Machine-readable truth beats prose.
- Data truth and schema definition are different layers. Do not confuse `.schema.yaml` with runtime truth.
- `tests/fixtures/` and `tests/evals/` are validation inputs, not the source of truth.
- `README.md` and `SKILL.md` explain repo behavior; they do not define truth when a YAML truth file already exists.

### Runtime Contract

- Runtime must not require local `kubeblocks-addons` checkout.
- Runtime must not require local KubeBlocks core checkout.
- `example_refs` and `core_refs` are provenance, not runtime prerequisites.
- `.kubeblocks-agent/` and runtime state files are optional acceleration only. They are not required to use this repo.

### Compatibility

- Old `kubeblocks-addon-*`, `kubeblocks-create-cluster`, and old Day-2 skill names may remain callable as shims.
- Legacy names must not be reintroduced as the recommended primary path.
- If a legacy name remains, its mapping must stay explicit and machine-readable.

## Document Responsibilities

Keep these layers distinct.

### `README.md`

Use `README.md` for:

- installation
- runtime contract
- repo layout
- truth-layer overview
- validation entrypoints
- cold-start usage model

Do not turn `README.md` into the maintainer change checklist.

### `AGENTS.md`

Use `AGENTS.md` for:

- maintainer-only rules
- what must change together
- what validators must run
- what patterns are forbidden when editing the repo
- how to extend truth, shims, fixtures, and live-eval assets safely

This file should be stricter and more operational than `README.md`.

### `SKILL.md`

Use root `SKILL.md` for:

- route order
- hard routing rules
- recommendation-bundle contract
- common misroutes to prevent

Do not let root `SKILL.md` become a second maintainer guide.

## Truth Precedence

When a maintainer finds conflicting statements, resolve conflicts in this order:

1. `references/routing/route-matrix.yaml`
2. `references/routing/shim-map.yaml`
3. `references/coverage/engine-tier-map.yaml`
4. `references/coverage/engine-create-matrix.yaml`
5. `references/coverage/ops-capability-matrix.yaml`
6. `references/coverage/observability-capability-matrix.yaml`
7. `references/coverage/addon-capability-matrix.yaml`
8. `references/runtime/runtime-contract.yaml`
9. leaf `skills/*/SKILL.md`
10. `README.md` and other prose references
11. optional addon/core inspection and raw examples

If prose disagrees with truth YAML, fix the prose.

## Change Types And Mandatory Sync Rules

Before editing, decide what kind of change you are making. Then update the full slice, not only the most visible file.

### 1. Routing change

Examples:

- changing the primary next hop
- forbidding a new wrong path
- changing how a legacy name maps forward

You must update:

- `references/routing/route-matrix.yaml`
- `references/routing/shim-map.yaml` if legacy mapping changes
- root `SKILL.md` if route order or hard routing rules change
- affected leaf skills if their forbidden paths or next hops change
- `references/testing/path-migrations.md` if human-readable migration guidance changes
- relevant `tests/fixtures/routing/*`

You must run:

- `python3 scripts/check_route_drift.py`
- `python3 scripts/validate_skills.py`

### 2. Engine create-time change

Examples:

- changing default topology
- adding or removing a Tier-1 dedicated engine
- changing version strategy, sizing, or connection guidance

You must update:

- `references/coverage/engine-tier-map.yaml` if tier, family, entry skill, or priority changes
- `references/coverage/engine-create-matrix.yaml`
- `references/coverage/addon-capability-matrix.yaml` if support/evidence claims change
- the matching `skills/kubeblocks-engine-*/SKILL.md`
- `tests/fixtures/create-depth/tier1-skill-contract.yaml` if Tier-1 contract changes
- relevant `tests/fixtures/routing/tier1/*.yaml` when route expectations change

You must run:

- `python3 scripts/validate_skills.py`
- `python3 scripts/check_addon_coverage.py --addons-repo <path>` when addon coverage truth changed
- `python3 scripts/check_route_drift.py` when route semantics changed

### 3. Day-2 capability change

Examples:

- adding support for restart, scale, reconfigure, restore, or expose
- changing whether an action is `supported`, `partial`, or `unsupported`

You must update:

- `references/coverage/ops-capability-matrix.yaml`
- `references/coverage/addon-capability-matrix.yaml` if `supported_ops` changed
- the matching `skills/kubeblocks-op-*/SKILL.md`
- relevant engine entry if next-hop guidance changed
- shim skill if old name remains callable

You must run:

- `python3 scripts/check_ops_coverage.py --addons-repo <path>` when ops truth changed
- `python3 scripts/validate_skills.py`

### 4. Observability change

Examples:

- changing readiness ceiling
- changing exporter presence
- changing bootstrap vs existing-stack routing

You must update:

- `references/coverage/observability-capability-matrix.yaml`
- `references/coverage/addon-capability-matrix.yaml` if exporter or observability evidence changed
- `skills/kubeblocks-observability-router/SKILL.md`
- `skills/kubeblocks-observability-existing-stack/SKILL.md` or `skills/kubeblocks-observability-bootstrap-stack/SKILL.md` if branch logic changed
- engine entries if their observability next-hop changed

You must run:

- `python3 scripts/validate_skills.py`
- `python3 scripts/check_route_drift.py` if routing semantics changed

### 5. Compatibility shim change

Examples:

- retiring a legacy name
- changing what a legacy skill forwards to
- clarifying old-to-new path migration

You must update:

- `references/routing/shim-map.yaml`
- `references/testing/path-migrations.md`
- the legacy shim skill under `skills/`
- `tests/fixtures/migrations/v1-shims.yaml` if fixture coverage changes

You must run:

- `python3 scripts/check_route_drift.py`
- `python3 scripts/validate_skills.py`

### 6. Top-level semantic change

Examples:

- changing runtime contract
- changing truth precedence
- changing the mainline control flow

You must update together:

- `README.md`
- `AGENTS.md`
- `SKILL.md`

Do not update only one of the three when the top-level model changed.

You must also check whether:

- routing truth needs changes
- live-eval rubric language should change
- maintainer validation instructions in README drifted

### 7. Live-eval change

Examples:

- changing eval schema
- changing severity policy
- adding or modifying scenarios or sample reports

You must update only within the approved slice.

Current frozen baseline:

- `tests/evals/schemas/eval-case.schema.yaml`
- `tests/evals/schemas/eval-step-report.schema.yaml`
- `tests/evals/rubrics/live-eval-rubric.yaml`
- `tests/evals/scenarios/postgresql-create-restart-observability-ack-multiaz.yaml`
- `tests/evals/reports/case-a-postgresql.sample.yaml`

Rules:

- Do not silently widen v0 into scripts, suites, or extra scenarios.
- `live-compatibility-drift` remains `conditional`, not observation-only.
- `verification-gap` remains `conditional`.
- Keep repo-completeness validators and live-eval assets as separate test lines.

If you intentionally move beyond v0, make that a new batch with an explicit scope decision.

## Writing Rules For Skills

### Root router

- Keep root `SKILL.md` router-only.
- It should decide next hop, not teach the whole repo again.

### Engine entries

- Tier-1 engine skills must be self-contained enough to complete the main create path.
- Do not send a cold-start agent back to raw addon examples to recover missing create-time guidance.
- Keep a real minimal create path in the skill, not only headings.
- Use upstream examples as parity evidence, not as the primary runtime recipe.

### Capability entries

- `kubeblocks-op-*` skills are the primary Day-2 surface.
- Make support boundaries explicit.
- When support is matrix-governed, say that clearly instead of implying universal support.

### Observability entries

- Speak in readiness levels: `metrics-ready`, `scrape-ready`, `dashboard-ready`, `alerting-ready`.
- Do not overclaim delivered monitoring when only exporter or endpoint readiness exists.

### Legacy shim entries

- Keep them short.
- State the new primary entry clearly.
- Do not let them evolve into parallel mainline documentation.

## Evidence Rules

When a support claim changes, capture why it is true.

- Prefer `docs_refs`, `example_refs`, and `core_refs` where schema supports them.
- Keep those fields as provenance.
- Do not write leaf skills that require the runtime agent to go inspect those references before acting.
- If official public docs and repo truth disagree, reconcile the repo truth and then update the prose.

## Validation Rules

At minimum, maintainers should run the validators touched by the change type.

Common validators:

- `python3 scripts/validate_skills.py`
- `python3 scripts/check_route_drift.py`
- `python3 scripts/check_addon_coverage.py --addons-repo <path>`
- `python3 scripts/check_ops_coverage.py --addons-repo <path>`

General rule:

- repo-local doc or skill wording changes should still run `validate_skills.py`
- route-affecting changes should run `check_route_drift.py`
- addon truth changes should run `check_addon_coverage.py`
- ops truth changes should run `check_ops_coverage.py`

If you changed YAML under `references/` or `tests/evals/`, also make sure it parses cleanly.

## Things Maintainers Must Not Do

- Do not treat workspace drafts as repo fact.
- Do not claim a batch is merged before checking actual `main`.
- Do not widen scope mid-batch without explicitly updating the cut list.
- Do not create new executable family skills just because taxonomy feels convenient.
- Do not let legacy names become the recommended path again.
- Do not add a runtime dependency on addon/core checkouts.
- Do not infer support from prose when a truth file exists.
- Do not ship top-level semantic changes in only one of `README.md`, `AGENTS.md`, or `SKILL.md`.

## Definition Of Done

A maintainer change is done only when all of the following are true:

- the repo still supports the cold-start runtime contract
- truth files, skills, fixtures, and top-level docs are aligned
- Tier-1 engines still route through dedicated entries
- legacy paths are still explicit and controlled
- validators relevant to the changed slice are green
- the repo became easier for a cold-start agent to use, not more dependent on maintainer memory

If in doubt, optimize for:

**less guessing, fewer hidden prerequisites, stronger machine-readable truth, and narrower, safer main paths.**
