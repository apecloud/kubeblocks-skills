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
- Use [references/testing/scenario-matrix.md](references/testing/scenario-matrix.md) and [tests/fixtures/routes.json](tests/fixtures/routes.json) as the initial routing regression baseline.

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

This repository is being organized into **five layers**:

1. **Router**
   Root [SKILL.md](SKILL.md) decides the next hop only.
2. **Preflight**
   Environment readiness and recommendation bundle generation before first-time provisioning.
3. **Engine Entry**
   High-frequency engines keep their own entry skills and only retain engine-specific decisions.
4. **Ops**
   Day-2 operations for existing clusters.
5. **Observability**
   Separate paths for integrating with an existing monitoring stack vs bootstrapping a new one.

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
| [kubeblocks-manage-addons](./skills/kubeblocks-manage-addons/SKILL.md) | Install, uninstall, and upgrade database engine addons. |

### Engine Entry

| Skill | Purpose |
|-------|---------|
| [kubeblocks-addon-mysql](./skills/kubeblocks-addon-mysql/SKILL.md) | MySQL entry with topology, version, storage, and sizing decisions. |
| [kubeblocks-addon-postgresql](./skills/kubeblocks-addon-postgresql/SKILL.md) | PostgreSQL entry with topology, version, storage, and sizing decisions. |
| [kubeblocks-addon-redis](./skills/kubeblocks-addon-redis/SKILL.md) | Redis entry. |
| [kubeblocks-addon-mongodb](./skills/kubeblocks-addon-mongodb/SKILL.md) | MongoDB entry. |
| [kubeblocks-addon-kafka](./skills/kubeblocks-addon-kafka/SKILL.md) | Kafka entry. |
| [kubeblocks-addon-elasticsearch](./skills/kubeblocks-addon-elasticsearch/SKILL.md) | Elasticsearch entry. |
| [kubeblocks-addon-milvus](./skills/kubeblocks-addon-milvus/SKILL.md) | Milvus entry. |
| [kubeblocks-addon-qdrant](./skills/kubeblocks-addon-qdrant/SKILL.md) | Qdrant entry. |
| [kubeblocks-addon-rabbitmq](./skills/kubeblocks-addon-rabbitmq/SKILL.md) | RabbitMQ entry. |
| [kubeblocks-create-cluster](./skills/kubeblocks-create-cluster/SKILL.md) | `other-addons` fallback only. Not for high-frequency engines. |
| [kubeblocks-delete-cluster](./skills/kubeblocks-delete-cluster/SKILL.md) | Safe deletion path. |

### Ops

| Skill | Purpose |
|-------|---------|
| [kubeblocks-cluster-lifecycle](./skills/kubeblocks-cluster-lifecycle/SKILL.md) | Stop, start, and restart clusters. |
| [kubeblocks-vertical-scaling](./skills/kubeblocks-vertical-scaling/SKILL.md) | Scale CPU and memory. |
| [kubeblocks-horizontal-scaling](./skills/kubeblocks-horizontal-scaling/SKILL.md) | Add or remove replicas or shards. |
| [kubeblocks-volume-expansion](./skills/kubeblocks-volume-expansion/SKILL.md) | Expand storage. |
| [kubeblocks-reconfigure-parameters](./skills/kubeblocks-reconfigure-parameters/SKILL.md) | Change database parameters. |
| [kubeblocks-minor-version-upgrade](./skills/kubeblocks-minor-version-upgrade/SKILL.md) | Upgrade engine versions. |
| [kubeblocks-switchover](./skills/kubeblocks-switchover/SKILL.md) | Planned primary-secondary switchover. |
| [kubeblocks-rebuild-replica](./skills/kubeblocks-rebuild-replica/SKILL.md) | Rebuild failed replicas. |
| [kubeblocks-backup](./skills/kubeblocks-backup/SKILL.md) | Backup workflows. |
| [kubeblocks-restore](./skills/kubeblocks-restore/SKILL.md) | Restore workflows. |
| [kubeblocks-configure-tls](./skills/kubeblocks-configure-tls/SKILL.md) | TLS and mTLS. |
| [kubeblocks-manage-accounts](./skills/kubeblocks-manage-accounts/SKILL.md) | Accounts and passwords. |
| [kubeblocks-expose-service](./skills/kubeblocks-expose-service/SKILL.md) | External service exposure. |
| [kubeblocks-upgrade](./skills/kubeblocks-upgrade/SKILL.md) | Upgrade KubeBlocks itself. |

### Observability

| Skill | Purpose |
|-------|---------|
| [kubeblocks-setup-monitoring](./skills/kubeblocks-setup-monitoring/SKILL.md) | Compatibility shim / observability router. |
| [kubeblocks-observability-existing-stack](./skills/kubeblocks-observability-existing-stack/SKILL.md) | Integrate database metrics into an existing Prometheus/Grafana stack. |
| [kubeblocks-observability-bootstrap-stack](./skills/kubeblocks-observability-bootstrap-stack/SKILL.md) | Bootstrap a new monitoring stack when none exists. |

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

## Testing & Iteration Hooks

This repository now treats testability as part of the structure.

### Validation Script

Run:

```bash
python3 scripts/validate_skills.py
```

It checks:

- frontmatter presence and version fields
- relative Markdown links in the root README/router and touched skill files
- route fixtures point to existing skills
- route fixtures declare both expected and prohibited next hops

### Initial Routing Fixtures

See [tests/fixtures/routes.json](tests/fixtures/routes.json) for the first regression cases:

- ACK multi-AZ + PostgreSQL/MySQL must go through `preflight`
- existing Prometheus/Grafana must route to `observability-existing-stack`
- unknown engines may use the `other-addons` fallback

### Path Migrations

[references/testing/path-migrations.md](references/testing/path-migrations.md) is the single source of truth for:

- old path / new path migrations
- customer-visible vs internal-only changes
- shim / fallback behavior
- optional one-liner and do-not-say guidance

## Contributing

When changing routing or skill boundaries:

1. Update [SKILL.md](SKILL.md) if the next-hop logic changes.
2. Update the affected leaf skills.
3. Update [references/testing/scenario-matrix.md](references/testing/scenario-matrix.md) and [tests/fixtures/routes.json](tests/fixtures/routes.json).
4. Update [references/testing/path-migrations.md](references/testing/path-migrations.md) if a path or recommendation changed.
5. Run `python3 scripts/validate_skills.py`.

## License

[Apache 2.0](LICENSE)
