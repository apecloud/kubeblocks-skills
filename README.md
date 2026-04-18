# KubeBlocks Agent Skills

Give AI agents a structured way to provision, operate, and observe databases on Kubernetes with KubeBlocks.

This repository is being shaped for three goals:

1. **Reliable routing for AI**
   The root skill should deterministically choose the next hop instead of mixing routing and long-form explanation.
2. **Safe provisioning**
   Database rollout readiness should be checked before engine-specific provisioning starts.
3. **Structured iteration**
   Repository structure, fixtures, and validation hooks should make future refactors testable and reviewable.

## Quick Start

- Use [SKILL.md](SKILL.md) as the top-level router.
- Use the leaf skills under [skills/](skills/) for concrete workflows.
- Use [references/testing/scenario-matrix.md](references/testing/scenario-matrix.md), [references/routing/shim-map.yaml](references/routing/shim-map.yaml), and the Tier-1 routing fixtures under [tests/fixtures/routing/tier1/](tests/fixtures/routing/tier1/) as the initial regression baseline.

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

For local installs, prefer a **stable user-level path** such as `~/.agents/skills/kubeblocks`. Avoid symlinking the active global skill path to an ephemeral agent workspace.

## Architecture

The target structure is not "one addon = one primary entry." The target is:

`root router -> environment gate(cluster/install/preflight) -> create path(dedicated engine | generic fallback) -> capability layers(ops/security/backup/observability) -> troubleshoot/recovery`

Key rules:

- `skills/` contains executable entries only.
- `references/coverage|routing|testing` contains static truths and human-readable contracts.
- `tests/fixtures/` contains machine-runnable cases only.
- `scripts/` validates drift between router, truths, fixtures, and docs.
- `family` stays a taxonomy/reference layer, not a cold-start create-time primary entry.

## Skill Catalog

### Router

| Skill | Purpose |
|-------|---------|
| [kubeblocks](./SKILL.md) | Router only. Decides the next hop. |

### Bootstrap & Readiness

| Skill | Purpose |
|-------|---------|
| [kubeblocks-create-local-k8s-cluster](./skills/kubeblocks-create-local-k8s-cluster/SKILL.md) | Create a local Kubernetes test cluster using Kind, Minikube, or k3d. |
| [kubeblocks-install](./skills/kubeblocks-install/SKILL.md) | Install the KubeBlocks operator. |
| [kubeblocks-preflight](./skills/kubeblocks-preflight/SKILL.md) | Check rollout readiness and emit an environment profile / recommendation bundle. |

### Engine Entry

| Skill | Purpose |
|-------|---------|
| [kubeblocks-engine-mysql](./skills/kubeblocks-engine-mysql/SKILL.md) | Primary MySQL create-time entry. |
| [kubeblocks-engine-postgresql](./skills/kubeblocks-engine-postgresql/SKILL.md) | Primary PostgreSQL create-time entry. |
| [kubeblocks-engine-redis](./skills/kubeblocks-engine-redis/SKILL.md) | Primary Redis create-time entry. |
| [kubeblocks-engine-mongodb](./skills/kubeblocks-engine-mongodb/SKILL.md) | Primary MongoDB create-time entry. |
| [kubeblocks-engine-kafka](./skills/kubeblocks-engine-kafka/SKILL.md) | Primary Kafka create-time entry. |
| [kubeblocks-engine-elasticsearch](./skills/kubeblocks-engine-elasticsearch/SKILL.md) | Primary Elasticsearch create-time entry. |
| [kubeblocks-engine-milvus](./skills/kubeblocks-engine-milvus/SKILL.md) | Primary Milvus create-time entry. |
| [kubeblocks-engine-qdrant](./skills/kubeblocks-engine-qdrant/SKILL.md) | Primary Qdrant create-time entry. |
| [kubeblocks-engine-rabbitmq](./skills/kubeblocks-engine-rabbitmq/SKILL.md) | Primary RabbitMQ create-time entry. |
| [kubeblocks-engine-clickhouse](./skills/kubeblocks-engine-clickhouse/SKILL.md) | Dedicated ClickHouse entry placeholder. |
| [kubeblocks-engine-mariadb](./skills/kubeblocks-engine-mariadb/SKILL.md) | Dedicated MariaDB entry placeholder. |
| [kubeblocks-engine-minio](./skills/kubeblocks-engine-minio/SKILL.md) | Dedicated MinIO entry placeholder. |
| [kubeblocks-engine-opensearch](./skills/kubeblocks-engine-opensearch/SKILL.md) | Dedicated OpenSearch entry placeholder. |
| [kubeblocks-engine-pulsar](./skills/kubeblocks-engine-pulsar/SKILL.md) | Dedicated Pulsar entry placeholder. |
| [kubeblocks-engine-tidb](./skills/kubeblocks-engine-tidb/SKILL.md) | Dedicated TiDB entry placeholder. |
| [kubeblocks-engine-generic](./skills/kubeblocks-engine-generic/SKILL.md) | `other-addons` fallback only. Not for the Tier-1 dedicated set. |

### Ops

| Skill | Purpose |
|-------|---------|
| [kubeblocks-op-lifecycle](./skills/kubeblocks-op-lifecycle/SKILL.md) | Primary lifecycle entry for stop, start, and restart. |
| [kubeblocks-op-vertical-scale](./skills/kubeblocks-op-vertical-scale/SKILL.md) | Primary CPU and memory scale entry. |
| [kubeblocks-op-horizontal-scale](./skills/kubeblocks-op-horizontal-scale/SKILL.md) | Primary replica or shard scale entry. |
| [kubeblocks-op-volume-expansion](./skills/kubeblocks-op-volume-expansion/SKILL.md) | Primary storage expansion entry. |
| [kubeblocks-op-reconfigure](./skills/kubeblocks-op-reconfigure/SKILL.md) | Primary parameter-change entry. |
| [kubeblocks-op-upgrade](./skills/kubeblocks-op-upgrade/SKILL.md) | Primary engine-upgrade entry. |
| [kubeblocks-op-switchover](./skills/kubeblocks-op-switchover/SKILL.md) | Primary planned switchover entry. |
| [kubeblocks-op-backup](./skills/kubeblocks-op-backup/SKILL.md) | Primary backup entry. |
| [kubeblocks-op-restore](./skills/kubeblocks-op-restore/SKILL.md) | Primary restore entry. |
| [kubeblocks-op-expose](./skills/kubeblocks-op-expose/SKILL.md) | Primary external service exposure entry. |
| [kubeblocks-delete-cluster](./skills/kubeblocks-delete-cluster/SKILL.md) | Safe deletion path. |
| [kubeblocks-upgrade](./skills/kubeblocks-upgrade/SKILL.md) | KubeBlocks operator upgrade. |
| [kubeblocks-configure-tls](./skills/kubeblocks-configure-tls/SKILL.md) | TLS and mTLS. |
| [kubeblocks-manage-accounts](./skills/kubeblocks-manage-accounts/SKILL.md) | Accounts and passwords. |
| [kubeblocks-rebuild-replica](./skills/kubeblocks-rebuild-replica/SKILL.md) | Replica rebuild / recovery support. |

### Observability

| Skill | Purpose |
|-------|---------|
| [kubeblocks-observability-router](./skills/kubeblocks-observability-router/SKILL.md) | Primary observability router. |
| [kubeblocks-observability-existing-stack](./skills/kubeblocks-observability-existing-stack/SKILL.md) | Integrate database metrics into an existing Prometheus/Grafana stack. |
| [kubeblocks-observability-bootstrap-stack](./skills/kubeblocks-observability-bootstrap-stack/SKILL.md) | Bootstrap a new monitoring stack when none exists. |
| [kubeblocks-setup-monitoring](./skills/kubeblocks-setup-monitoring/SKILL.md) | Legacy compatibility shim. |

### Troubleshooting

| Skill | Purpose |
|-------|---------|
| [kubeblocks-troubleshoot](./skills/kubeblocks-troubleshoot/SKILL.md) | Diagnose broken or stuck clusters. |

## Shared References

The repository keeps shared references under [references/](references/):

- [references/common/skill-skeleton.md](references/common/skill-skeleton.md)
- [references/common/decision-patterns.md](references/common/decision-patterns.md)
- [references/common/frontmatter-schema.md](references/common/frontmatter-schema.md)
- [references/testing/scenario-matrix.md](references/testing/scenario-matrix.md)
- [references/testing/smoke-checklist.md](references/testing/smoke-checklist.md)
- [references/testing/path-migrations.md](references/testing/path-migrations.md)
- [references/routing/shim-map.yaml](references/routing/shim-map.yaml)

## Testing & Iteration Hooks

This repository now treats testability as part of the structure.

### Validation Script

Run:

```bash
python3 scripts/validate_skills.py
python3 scripts/check_addon_coverage.py
python3 scripts/check_ops_coverage.py
python3 scripts/check_route_drift.py
```

It checks:

- frontmatter presence and version fields
- relative Markdown links in the router, README, skill files, and routing/testing references
- Tier-1 routing fixtures point to existing skills or approved reference-only families
- shim fixtures stay aligned with `references/routing/shim-map.yaml`
- addon, ops, and routing truth stay consistent with the Tier-1 baseline

### Initial Routing Fixtures

See the machine-runnable fixtures under [tests/fixtures/](tests/fixtures/):

- [tests/fixtures/routing/tier1/](tests/fixtures/routing/tier1/) for allowed and forbidden Tier-1 create-time routes
- [tests/fixtures/migrations/v1-shims.yaml](tests/fixtures/migrations/v1-shims.yaml) for legacy-name shim coverage
- [tests/fixtures/coverage/tier1-required-engines.yaml](tests/fixtures/coverage/tier1-required-engines.yaml) and [tests/fixtures/coverage/tier1-min-ops.yaml](tests/fixtures/coverage/tier1-min-ops.yaml) for Tier-1 coverage minimums

### Path Migrations

[references/testing/path-migrations.md](references/testing/path-migrations.md) is the single source of truth for:

- old path / new path migrations
- customer-visible vs internal-only changes
- shim / fallback behavior
- optional one-liner and do-not-say guidance

## Runtime State Protocol

Cold-start agents should not depend on pre-existing memory files, but long-running tasks benefit from structured runtime state outside the repo. Recommended workspace-local layout:

- `.kubeblocks-agent/state/environment-profile.yaml`
- `.kubeblocks-agent/state/cluster-<name>.yaml`
- `.kubeblocks-agent/state/route-context.yaml`
- `.kubeblocks-agent/logs/<timestamp>.jsonl`
- `.kubeblocks-agent/HANDOFF.md`

These files are runtime artifacts, not static truths. Keep them out of the skill repo and refresh them when the environment changes.

## Contributing

When changing routing or skill boundaries:

1. Update [SKILL.md](SKILL.md) if the next-hop logic changes.
2. Update the affected leaf skills.
3. Update the relevant truth files under `references/coverage/` and `references/routing/`.
4. Update [references/testing/path-migrations.md](references/testing/path-migrations.md) and `references/routing/shim-map.yaml` if a path or recommendation changed.
5. Update the relevant fixtures under `tests/fixtures/`.
6. Run all four checks:
   - `python3 scripts/validate_skills.py`
   - `python3 scripts/check_addon_coverage.py`
   - `python3 scripts/check_ops_coverage.py`
   - `python3 scripts/check_route_drift.py`

## License

[Apache 2.0](LICENSE)
