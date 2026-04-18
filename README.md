# KubeBlocks Skills for Cold-Start Agents

This repository is for one outcome:

**a cold-start agent should be able to act like a practical KubeBlocks operator with minimal guessing.**

That means the repo should help an agent:

1. decide which phase it is in
2. choose the right next hop
3. know what is supported and what is not
4. avoid bouncing between old names, raw addon examples, and long-form prose

This repo is therefore closer to an agent operating system than a static document set.

## What A Cold-Start Agent Should Do

The default flow is:

`root router -> environment gate -> dedicated engine | generic fallback -> capability layers -> observability -> troubleshoot/recovery`

In practice:

1. Start at [SKILL.md](SKILL.md).
2. Decide whether the task is:
   - cluster bootstrap
   - KubeBlocks install
   - first-time database create
   - existing-cluster operation
   - observability
   - troubleshooting
3. If the request is create-time and the environment is not already understood, route through [kubeblocks-preflight](skills/kubeblocks-preflight/SKILL.md).
4. If the engine is in the Tier-1 dedicated set, use its dedicated `kubeblocks-engine-*` entry.
5. Only use [kubeblocks-engine-generic](skills/kubeblocks-engine-generic/SKILL.md) for `other-addons` fallback.
6. Once a cluster exists, move into capability-layer entries such as `kubeblocks-op-*`, access-security, observability, or troubleshooting.

## What This Repo Is Not

This repo is not trying to:

- turn `family` into a create-time primary entry
- encode every addon example as canonical truth
- make runtime memory files mandatory
- widen coverage faster than the agent can reliably use it

The priority is always: **high-frequency paths with low ambiguity first**.

## Install

**One-liner (requires Node.js):**

```bash
npx skills add https://github.com/apecloud/kubeblocks-skills
```

**Or install for a specific platform:**

| Platform | Install |
|----------|---------|
| **Cursor** (2.4+) | Settings → Rules → Add Rule → Remote Rule (GitHub) → `https://github.com/apecloud/kubeblocks-skills` |
| **OpenAI Codex** | `$skill-installer https://github.com/apecloud/kubeblocks-skills` |
| **Claude Code** | `git clone https://github.com/apecloud/kubeblocks-skills ~/.claude/skills/kubeblocks` |
| **OpenClaw / Other** | `git clone https://github.com/apecloud/kubeblocks-skills ~/.agents/skills/kubeblocks` |

For local installs, prefer a stable user-level path such as `~/.agents/skills/kubeblocks`. Avoid pointing the live global skill path at an ephemeral agent workspace.

## Repository Layout

### `skills/`

Executable entries only.

- root router
- install / preflight / local-cluster bootstrap
- dedicated engine entries
- generic fallback
- shared capability-layer entries
- observability entries
- troubleshooting and recovery entries
- legacy shims that remain callable but are not recommended as primary paths

### `references/`

Static truth, contracts, and human-readable support material.

- `references/routing/`
- `references/coverage/`
- `references/testing/`
- `references/runtime/`
- `references/templates/`

### `tests/fixtures/`

Machine-runnable cases only.

- route coverage
- create-depth contracts
- legacy shim coverage
- Tier-1 minimums

### `scripts/`

Drift and coverage validators. These are how the repo proves that docs, skills, truth files, and fixtures are still aligned.

## Truth Layers

Cold-start agents should prefer machine-readable truth before prose.

### Routing Truth

- [references/routing/route-matrix.yaml](references/routing/route-matrix.yaml)
- [references/routing/shim-map.yaml](references/routing/shim-map.yaml)

Use these to answer:

- what the next hop is
- which paths are forbidden
- how old names map to current names

### Create-Time Truth

- [references/coverage/engine-create-matrix.yaml](references/coverage/engine-create-matrix.yaml)

Use this to answer:

- default topology
- allowed topology options
- preflight requirements
- sizing profiles
- connection methods
- next hops
- forbidden create paths

### Capability Truth

- [references/coverage/ops-capability-matrix.yaml](references/coverage/ops-capability-matrix.yaml)
- [references/coverage/observability-capability-matrix.yaml](references/coverage/observability-capability-matrix.yaml)
- [references/coverage/addon-capability-matrix.yaml](references/coverage/addon-capability-matrix.yaml)

Use these to answer:

- whether a Day-2 action is actually supported
- what observability readiness ceiling exists for a given engine
- what docs, examples, and core evidence support a claim

### Runtime Truth

- [references/runtime/runtime-contract.yaml](references/runtime/runtime-contract.yaml)

This defines optional repo-external runtime state and handoff structure. It is an acceleration layer, not a cold-start requirement.

## Primary Engine Paths

The current Tier-1 dedicated set is:

- MySQL
- PostgreSQL
- Redis
- MongoDB
- Kafka
- Elasticsearch
- Milvus
- Qdrant
- RabbitMQ
- ClickHouse
- MariaDB
- MinIO
- OpenSearch
- Pulsar
- TiDB

Each of these should be entered through its dedicated `kubeblocks-engine-*` skill, not through generic fallback and not through a family label.

## Capability Layers

Once a cluster exists, stop using create-time reasoning as the main control surface.

Use:

- `kubeblocks-op-*` for lifecycle, scaling, storage growth, reconfigure, backup, restore, expose, switchover, and engine upgrade
- [kubeblocks-manage-accounts](skills/kubeblocks-manage-accounts/SKILL.md) for account/password handling
- [kubeblocks-configure-tls](skills/kubeblocks-configure-tls/SKILL.md) for TLS and mTLS
- [kubeblocks-rebuild-replica](skills/kubeblocks-rebuild-replica/SKILL.md) for supported replica-repair flows
- [kubeblocks-observability-router](skills/kubeblocks-observability-router/SKILL.md) for monitoring path selection
- [kubeblocks-troubleshoot](skills/kubeblocks-troubleshoot/SKILL.md) when support or state is unclear

## Examples Are Evidence, Not Primary Truth

The repo still uses `kubeblocks-addons` and KubeBlocks docs as evidence. It does **not** want the cold-start agent to depend on raw example files as its primary decision source.

The intended order is:

1. route correctly
2. read the relevant truth file
3. use the leaf skill's create/capability contract
4. use addon examples only as evidence anchors or parity checks

This is how the repo avoids overfitting to the current example directory layout.

## Validation

Run:

```bash
python3 scripts/validate_skills.py
python3 scripts/check_route_drift.py

# Cross-repo checks. These require a kubeblocks-addons checkout.
python3 scripts/check_addon_coverage.py --addons-repo ../kubeblocks-addons
python3 scripts/check_ops_coverage.py --addons-repo ../kubeblocks-addons
```

Validation is split into two classes:

- `validate_skills.py` and `check_route_drift.py`
  repo-local checks that should work in a clean clone
- `check_addon_coverage.py` and `check_ops_coverage.py`
  cross-repo checks that require `kubeblocks-addons`

The validators currently enforce:

- router and README alignment
- shim-map and path-migrations alignment
- Tier-1 route truth
- Tier-1 create-depth contracts
- addon and ops coverage truth
- runtime contract/template alignment

## Runtime State Protocol

Recommended repo-external layout:

- `.kubeblocks-agent/state/environment-profile.yaml`
- `.kubeblocks-agent/state/route-context.yaml`
- `.kubeblocks-agent/state/cluster-<name>.yaml`
- `.kubeblocks-agent/logs/<timestamp>.jsonl`
- `.kubeblocks-agent/HANDOFF.md`

These files help long-running tasks and handoff, but they must remain optional. A cold-start agent should still function with only the repo itself.

Templates live under [references/templates/](references/templates/). The contract lives in [references/runtime/runtime-contract.yaml](references/runtime/runtime-contract.yaml).

## Editing Rules

If you change routing, support claims, or primary skill boundaries, update all relevant layers together:

1. [SKILL.md](SKILL.md)
2. the affected skill entries under [skills/](skills/)
3. the matching truth files in `references/routing/` and `references/coverage/`
4. the matching fixtures in [tests/fixtures/](tests/fixtures/)
5. the validators in [scripts/](scripts/)

Do not merge a change that only updates prose while leaving truth, fixtures, or scripts behind.

## Related Files

- [AGENTS.md](AGENTS.md) for direct repository usage instructions aimed at agents
- [SKILL.md](SKILL.md) for the root router
- [references/testing/path-migrations.md](references/testing/path-migrations.md) for human-readable path migration history
- [references/testing/scenario-matrix.md](references/testing/scenario-matrix.md) for scenario coverage
- [references/testing/smoke-checklist.md](references/testing/smoke-checklist.md) for basic manual verification

## License

[Apache 2.0](LICENSE)
