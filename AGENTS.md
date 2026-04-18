This repository is designed to make a **cold-start agent behave like a KubeBlocks database operator**, not like a generic documentation reader.

Runtime assumption:

- A user should be able to install **only this repo** and still use it.
- The cold-start runtime dependency is: **this repo + official public KubeBlocks docs**.
- `kubeblocks-addons` and KubeBlocks core repos are **maintainer evidence only**, not runtime prerequisites.
- If a runtime path still requires raw addon examples or core source checkout to make the main decision, treat that as a repo gap and fix the repo.

Start here:

1. Read the root [SKILL.md](SKILL.md).
2. Let it route you to the correct next hop.
3. Use the truth files under `references/` to confirm what is actually supported.
4. Use leaf skills under `skills/` to execute the specific workflow.

Core operating model:

- Mainline is:
  `router -> environment gate (cluster/install/preflight) -> dedicated engine | generic fallback -> capability layers -> troubleshoot/recovery`
- `family` is **reference-only taxonomy**. It is not a create-time primary path.
- Tier-1 engines should never fall back to generic or to legacy addon skills when a dedicated `kubeblocks-engine-*` entry exists.
- If environment readiness is unknown, run `kubeblocks-preflight` before first-time provisioning.

Truth precedence:

1. `references/routing/route-matrix.yaml`
2. `references/routing/shim-map.yaml`
3. `references/coverage/*.yaml`
4. `references/runtime/runtime-contract.yaml`
5. `skills/*/SKILL.md`
6. addon examples and legacy references as evidence only

Important constraints:

- Do not treat old `kubeblocks-addon-*`, `kubeblocks-create-cluster`, or old Day-2 names as the primary path when a new engine/op entry exists.
- Do not assume every engine supports the same Day-2, observability, access-security, or recovery actions.
- Do not use runtime memory as a prerequisite. `.kubeblocks-agent/` is optional acceleration, not repo truth.
- Do not infer support from prose alone when a machine-readable truth file exists.

Definition of success:

- A cold-start agent can choose the right path without guessing.
- A Tier-1 engine entry is enough to complete the main create path without stitching together README, legacy skills, and raw examples.
- Validation scripts and fixtures can prove the repo has not drifted away from that behavior.
