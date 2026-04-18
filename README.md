# KubeBlocks Agent Skills

Give a cold-start agent enough structure to install KubeBlocks, choose the right database path, operate supported Day-2 actions, and avoid the common wrong turns.

This repository is not trying to be a generic document dump. Its job is narrower and stricter:

> A single agent with only `kubeblocks-skills` should be able to decide the next safe hop, provision the right engine path, and only execute supported KubeBlocks operations without hidden tribal knowledge.

## If You Are a Cold-Start Agent

Start here:

1. If there is no Kubernetes cluster yet, go to [kubeblocks-create-local-k8s-cluster](./skills/kubeblocks-create-local-k8s-cluster/SKILL.md).
2. If Kubernetes exists but KubeBlocks is not installed, go to [kubeblocks-install](./skills/kubeblocks-install/SKILL.md).
3. If the user wants to create a database and rollout readiness is unknown, go to [kubeblocks-preflight](./skills/kubeblocks-preflight/SKILL.md) first.
4. After preflight, route create-time requests to a dedicated Tier-1 engine entry when one exists. Only use [kubeblocks-engine-generic](./skills/kubeblocks-engine-generic/SKILL.md) for `other-addons` fallback.
5. For an existing cluster, route to the right capability layer:
   `kubeblocks-op-*`, [kubeblocks-manage-accounts](./skills/kubeblocks-manage-accounts/SKILL.md), [kubeblocks-configure-tls](./skills/kubeblocks-configure-tls/SKILL.md), [kubeblocks-delete-cluster](./skills/kubeblocks-delete-cluster/SKILL.md), or [kubeblocks-upgrade](./skills/kubeblocks-upgrade/SKILL.md).
6. For monitoring and dashboards, start with [kubeblocks-observability-router](./skills/kubeblocks-observability-router/SKILL.md).
7. If state is unclear or the system is already broken, route to [kubeblocks-troubleshoot](./skills/kubeblocks-troubleshoot/SKILL.md) and only then consider recovery actions like [kubeblocks-rebuild-replica](./skills/kubeblocks-rebuild-replica/SKILL.md).

The root router in [SKILL.md](./SKILL.md) encodes this same next-hop order. README explains the why; root skill decides the hop.

## First-Principles Rules

These are the non-negotiable routing rules behind the current structure:

1. Environment uncertainty comes before engine choice.
   KubeBlocks failures usually come from storage, topology, scheduling, monitoring base, or permissions, not from YAML syntax. That is why [kubeblocks-preflight](./skills/kubeblocks-preflight/SKILL.md) exists.
2. Create-time guidance and Day-2 guidance are different layers.
   Engine entry skills answer topology, version, storage, sizing, connection, and next hop. They are not supposed to absorb every Day-2 action.
3. `family` is reference-only taxonomy.
   It can explain similarity, coverage grouping, or fallback intent, but it must not become a cold-start create-time execution entry. In this repo, `family` is not a cold-start create-time primary entry.
4. Tier-1 engines must stay dedicated.
   They must not route back to generic or to a family explanation layer.
5. Support claims come from data truth, not prose.
   Whether an engine supports backup, switchover, scaling, or monitoring exporter should come from the coverage matrices, not from guesswork inside a skill body.
6. Legacy names may stay callable, but only as shims.
   Old `kubeblocks-addon-*`, `kubeblocks-create-cluster`, and old Day-2 names exist for compatibility, not as recommended primary paths.

## Main Execution Flow

The current intended flow is:

`root router -> environment gate(cluster/install/preflight) -> dedicated engine | generic fallback -> capability layers(ops/security/backup/observability) -> troubleshoot/recovery`

That means:

- [SKILL.md](./SKILL.md) is router-only.
- [kubeblocks-preflight](./skills/kubeblocks-preflight/SKILL.md) is the environment gate for first-time rollout.
- `kubeblocks-engine-*` is the create-time layer.
- `kubeblocks-op-*` plus a few non-op capability skills form the shared Day-2 layer.
- observability stays separate from create-time and from generic ops.
- troubleshoot/recovery is a parallel safe branch whenever the current state is unknown or broken.

## Tier-1 Dedicated Engines

These engines must have dedicated create-time entries and must not default back to generic or family:

- [kubeblocks-engine-mysql](./skills/kubeblocks-engine-mysql/SKILL.md)
- [kubeblocks-engine-postgresql](./skills/kubeblocks-engine-postgresql/SKILL.md)
- [kubeblocks-engine-redis](./skills/kubeblocks-engine-redis/SKILL.md)
- [kubeblocks-engine-mongodb](./skills/kubeblocks-engine-mongodb/SKILL.md)
- [kubeblocks-engine-kafka](./skills/kubeblocks-engine-kafka/SKILL.md)
- [kubeblocks-engine-elasticsearch](./skills/kubeblocks-engine-elasticsearch/SKILL.md)
- [kubeblocks-engine-milvus](./skills/kubeblocks-engine-milvus/SKILL.md)
- [kubeblocks-engine-qdrant](./skills/kubeblocks-engine-qdrant/SKILL.md)
- [kubeblocks-engine-rabbitmq](./skills/kubeblocks-engine-rabbitmq/SKILL.md)
- [kubeblocks-engine-clickhouse](./skills/kubeblocks-engine-clickhouse/SKILL.md)
- [kubeblocks-engine-mariadb](./skills/kubeblocks-engine-mariadb/SKILL.md)
- [kubeblocks-engine-minio](./skills/kubeblocks-engine-minio/SKILL.md)
- [kubeblocks-engine-opensearch](./skills/kubeblocks-engine-opensearch/SKILL.md)
- [kubeblocks-engine-pulsar](./skills/kubeblocks-engine-pulsar/SKILL.md)
- [kubeblocks-engine-tidb](./skills/kubeblocks-engine-tidb/SKILL.md)

For engines outside that set, use [kubeblocks-engine-generic](./skills/kubeblocks-engine-generic/SKILL.md) as the `other-addons` fallback only after preflight.

## Capability Layers

### Environment Gate

- [kubeblocks-create-local-k8s-cluster](./skills/kubeblocks-create-local-k8s-cluster/SKILL.md)
- [kubeblocks-install](./skills/kubeblocks-install/SKILL.md)
- [kubeblocks-preflight](./skills/kubeblocks-preflight/SKILL.md)

### Shared Day-2 Ops

- [kubeblocks-op-lifecycle](./skills/kubeblocks-op-lifecycle/SKILL.md)
- [kubeblocks-op-horizontal-scale](./skills/kubeblocks-op-horizontal-scale/SKILL.md)
- [kubeblocks-op-vertical-scale](./skills/kubeblocks-op-vertical-scale/SKILL.md)
- [kubeblocks-op-volume-expansion](./skills/kubeblocks-op-volume-expansion/SKILL.md)
- [kubeblocks-op-reconfigure](./skills/kubeblocks-op-reconfigure/SKILL.md)
- [kubeblocks-op-backup](./skills/kubeblocks-op-backup/SKILL.md)
- [kubeblocks-op-restore](./skills/kubeblocks-op-restore/SKILL.md)
- [kubeblocks-op-expose](./skills/kubeblocks-op-expose/SKILL.md)
- [kubeblocks-op-switchover](./skills/kubeblocks-op-switchover/SKILL.md)
- [kubeblocks-op-upgrade](./skills/kubeblocks-op-upgrade/SKILL.md)

### Shared Non-Op Capability Skills

- [kubeblocks-manage-accounts](./skills/kubeblocks-manage-accounts/SKILL.md)
- [kubeblocks-configure-tls](./skills/kubeblocks-configure-tls/SKILL.md)
- [kubeblocks-delete-cluster](./skills/kubeblocks-delete-cluster/SKILL.md)
- [kubeblocks-upgrade](./skills/kubeblocks-upgrade/SKILL.md)

### Observability

- [kubeblocks-observability-router](./skills/kubeblocks-observability-router/SKILL.md)
- [kubeblocks-observability-existing-stack](./skills/kubeblocks-observability-existing-stack/SKILL.md)
- [kubeblocks-observability-bootstrap-stack](./skills/kubeblocks-observability-bootstrap-stack/SKILL.md)
- [kubeblocks-setup-monitoring](./skills/kubeblocks-setup-monitoring/SKILL.md) as a legacy shim only

### Troubleshoot / Recovery

- [kubeblocks-troubleshoot](./skills/kubeblocks-troubleshoot/SKILL.md)
- [kubeblocks-rebuild-replica](./skills/kubeblocks-rebuild-replica/SKILL.md)

## Static Truth Vs Executable Skills

The repository is intentionally split into four layers:

- `skills/`: executable entries only
- `references/coverage|routing|testing`: static truths, contracts, and human-readable guidance
- `tests/fixtures/`: machine-runnable route, migration, and coverage cases
- `scripts/`: consistency checks across skills, truth files, fixtures, and docs

The important truth files are:

- [references/coverage/engine-tier-map.yaml](./references/coverage/engine-tier-map.yaml)
- [references/coverage/addon-capability-matrix.yaml](./references/coverage/addon-capability-matrix.yaml)
- [references/coverage/ops-capability-matrix.yaml](./references/coverage/ops-capability-matrix.yaml)
- [references/routing/route-matrix.yaml](./references/routing/route-matrix.yaml)
- [references/routing/shim-map.yaml](./references/routing/shim-map.yaml)

The important human-facing references are:

- [references/planning/v2-structure-plan.md](./references/planning/v2-structure-plan.md)
- [references/testing/path-migrations.md](./references/testing/path-migrations.md)
- [references/testing/scenario-matrix.md](./references/testing/scenario-matrix.md)
- [references/testing/smoke-checklist.md](./references/testing/smoke-checklist.md)

## Legacy Names And Shims

Legacy names are still present because existing callers must not break immediately. But they are compatibility shims, not primary recommendations.

Examples:

- `kubeblocks-addon-mysql` -> `kubeblocks-engine-mysql`
- `kubeblocks-create-cluster` -> `kubeblocks-engine-generic`
- `kubeblocks-setup-monitoring` -> `kubeblocks-observability-router`
- old Day-2 names like `kubeblocks-backup` or `kubeblocks-horizontal-scaling` -> `kubeblocks-op-*`

Exact shim truth lives in [references/routing/shim-map.yaml](./references/routing/shim-map.yaml). The human-readable migration ledger is [references/testing/path-migrations.md](./references/testing/path-migrations.md). Route drift checks require those two to match pair-for-pair.

## Install

One-liner:

```bash
npx skills add https://github.com/apecloud/kubeblocks-skills
```

Platform-specific install:

| Platform | Install |
|----------|---------|
| Cursor (2.4+) | Settings -> Rules -> Add Rule -> Remote Rule (GitHub) -> `https://github.com/apecloud/kubeblocks-skills` |
| OpenAI Codex | `$skill-installer https://github.com/apecloud/kubeblocks-skills` |
| Claude Code | `git clone https://github.com/apecloud/kubeblocks-skills ~/.claude/skills/kubeblocks` |
| OpenClaw / Other | `git clone https://github.com/apecloud/kubeblocks-skills ~/.agents/skills/kubeblocks` |

For local installs, prefer a stable user-level path such as `~/.agents/skills/kubeblocks`. Do not point the active global skill path at an ephemeral agent workspace.

## Validation

Repo-local checks:

```bash
python3 scripts/validate_skills.py
python3 scripts/check_route_drift.py
```

Cross-repo checks:

```bash
python3 scripts/check_addon_coverage.py --addons-repo ../kubeblocks-addons
python3 scripts/check_ops_coverage.py --addons-repo ../kubeblocks-addons
```

Validation contract:

- `validate_skills.py` checks frontmatter, link integrity, fixture targets, and basic repo consistency.
- `check_route_drift.py` checks `SKILL.md`, `README.md`, `route-matrix.yaml`, `shim-map.yaml`, `path-migrations.md`, and Tier-1 fixtures for route drift.
- `check_addon_coverage.py` and `check_ops_coverage.py` are intentionally cross-repo. They require a local `kubeblocks-addons` checkout, either at the default sibling path `../kubeblocks-addons` or via `--addons-repo /path/to/kubeblocks-addons`.

## Runtime State Protocol

Cold-start agents must be able to work without pre-existing memory files. Runtime state is an optional acceleration layer, not a routing dependency.

Recommended workspace-local layout:

- `.kubeblocks-agent/state/environment-profile.yaml`
- `.kubeblocks-agent/state/route-context.yaml`
- `.kubeblocks-agent/state/cluster-<name>.yaml`
- `.kubeblocks-agent/logs/<timestamp>.jsonl`
- `.kubeblocks-agent/HANDOFF.md`

Templates live under [references/templates/](./references/templates/). Keep runtime artifacts out of the skill repo and refresh them when the environment changes.

## Contributing

When changing routes, boundaries, or support claims:

1. Update [SKILL.md](./SKILL.md) if next-hop routing changed.
2. Update the affected leaf skills under [skills/](./skills/).
3. Update the matching truth files under [references/coverage/](./references/coverage/) and [references/routing/](./references/routing/).
4. Update [references/testing/path-migrations.md](./references/testing/path-migrations.md) and [references/routing/shim-map.yaml](./references/routing/shim-map.yaml) together if a legacy recommendation or shim changed.
5. Update the relevant fixtures under [tests/fixtures/](./tests/fixtures/).
6. Run:
   - `python3 scripts/validate_skills.py`
   - `python3 scripts/check_route_drift.py`
   - `python3 scripts/check_addon_coverage.py --addons-repo ../kubeblocks-addons`
   - `python3 scripts/check_ops_coverage.py --addons-repo ../kubeblocks-addons`

## License

[Apache 2.0](./LICENSE)
