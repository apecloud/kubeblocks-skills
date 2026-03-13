# KubeBlocks Agent Skills

A collection of Agent Skills for managing [KubeBlocks](https://kubeblocks.io/) — the unified Kubernetes operator for 30+ database engines.

These skills work with any AI coding agent that supports markdown-based skill files (Cursor, Claude Code, OpenClaw, etc.).

## Quick Start

Point your agent to `kubeblocks-overview/SKILL.md` — it serves as a navigation hub that routes to the right skill for any task.

## Available Skills

### Navigation

| Skill | Description |
|-------|-------------|
| [kubeblocks-overview](./kubeblocks-overview/SKILL.md) | Navigate KubeBlocks capabilities and find the right skill for any database management task. |

### Setup & Infrastructure

| Skill | Description |
|-------|-------------|
| [kubeblocks-create-local-k8s-cluster](./kubeblocks-create-local-k8s-cluster/SKILL.md) | Create a local Kubernetes test cluster using Kind, Minikube, or k3d. |
| [kubeblocks-install](./kubeblocks-install/SKILL.md) | Install the KubeBlocks operator. Handles version selection, network detection, registry configuration. |
| [kubeblocks-manage-addons](./kubeblocks-manage-addons/SKILL.md) | Install, uninstall, and upgrade database engine addons. |

### Cluster Provisioning & Deletion

| Skill | Description |
|-------|-------------|
| [kubeblocks-create-cluster](./kubeblocks-create-cluster/SKILL.md) | Create a database cluster (generic entry point for all addons). |
| [kubeblocks-delete-cluster](./kubeblocks-delete-cluster/SKILL.md) | Safely delete a database cluster with pre-deletion checks. |

### Day-2 Operations

| Skill | Description |
|-------|-------------|
| [kubeblocks-cluster-lifecycle](./kubeblocks-cluster-lifecycle/SKILL.md) | Stop, start, and restart database clusters. |
| [kubeblocks-vertical-scaling](./kubeblocks-vertical-scaling/SKILL.md) | Scale CPU and memory resources. |
| [kubeblocks-horizontal-scaling](./kubeblocks-horizontal-scaling/SKILL.md) | Add/remove replicas or shards. |
| [kubeblocks-volume-expansion](./kubeblocks-volume-expansion/SKILL.md) | Expand persistent volume storage. |
| [kubeblocks-reconfigure-parameters](./kubeblocks-reconfigure-parameters/SKILL.md) | Modify database configuration parameters. |
| [kubeblocks-minor-version-upgrade](./kubeblocks-minor-version-upgrade/SKILL.md) | Upgrade database engine minor versions. |
| [kubeblocks-switchover](./kubeblocks-switchover/SKILL.md) | Perform planned primary-secondary switchover. |
| [kubeblocks-expose-service](./kubeblocks-expose-service/SKILL.md) | Expose databases externally via LoadBalancer or NodePort. |

### Data Protection

| Skill | Description |
|-------|-------------|
| [kubeblocks-backup](./kubeblocks-backup/SKILL.md) | Create on-demand, scheduled, and continuous backups. |
| [kubeblocks-restore](./kubeblocks-restore/SKILL.md) | Restore from backups with full restore or Point-in-Time Recovery. |

### Security

| Skill | Description |
|-------|-------------|
| [kubeblocks-manage-accounts](./kubeblocks-manage-accounts/SKILL.md) | Manage database passwords and password policies. |
| [kubeblocks-configure-tls](./kubeblocks-configure-tls/SKILL.md) | Configure TLS, custom certificates, and mTLS. |

### Observability

| Skill | Description |
|-------|-------------|
| [kubeblocks-setup-monitoring](./kubeblocks-setup-monitoring/SKILL.md) | Set up Prometheus monitoring and Grafana dashboards. |

### Engine-Specific Skills

| Skill | Description |
|-------|-------------|
| [kubeblocks-addon-mysql](./kubeblocks-addon-mysql/SKILL.md) | MySQL topologies (semi-sync, MGR, Orchestrator, ProxySQL variants). |
| [kubeblocks-addon-postgresql](./kubeblocks-addon-postgresql/SKILL.md) | PostgreSQL with Patroni-based HA replication. |
| [kubeblocks-addon-redis](./kubeblocks-addon-redis/SKILL.md) | Redis standalone, replication with Sentinel, and Redis Cluster sharding. |
| [kubeblocks-addon-mongodb](./kubeblocks-addon-mongodb/SKILL.md) | MongoDB ReplicaSet and Sharding topologies. |
| [kubeblocks-addon-kafka](./kubeblocks-addon-kafka/SKILL.md) | Apache Kafka combined and separated broker/controller modes. |

## Install

| Platform | Install |
|----------|---------|
| **Cursor** (2.4+) | Settings → Rules → Add Rule → Remote Rule (GitHub) → `https://github.com/apecloud/kubeblocks-skills` |
| **OpenAI Codex** | `$skill-installer https://github.com/apecloud/kubeblocks-skills` |
| **Claude Code** | `git clone https://github.com/apecloud/kubeblocks-skills ~/.claude/skills/kubeblocks` |
| **OpenClaw / Other** | `git clone https://github.com/apecloud/kubeblocks-skills ~/.agents/skills/kubeblocks` |

All skills follow the [Agent Skills](https://agentskills.io/) open standard and work with any agent that reads `SKILL.md` files.

## Skill Structure

```
skill-name/
├── SKILL.md          # Main instructions (entry point, < 500 lines)
└── reference.md      # Detailed reference (read on demand, optional)
```

- **SKILL.md**: Concise step-by-step workflow with YAML templates.
- **reference.md**: Detailed configuration options, addon-specific differences, and extended examples.

## Architecture

```
kubeblocks-overview ─────── Navigation hub
        │
        ├── Infrastructure: kubeblocks-create-local-k8s-cluster → kubeblocks-install → kubeblocks-manage-addons
        │
        ├── Provisioning:   kubeblocks-create-cluster ←→ kubeblocks-addon-{mysql,pg,redis,mongodb,kafka}
        │                   kubeblocks-delete-cluster
        │
        ├── Operations:     kubeblocks-cluster-lifecycle, kubeblocks-vertical-scaling,
        │                   kubeblocks-horizontal-scaling, kubeblocks-volume-expansion,
        │                   kubeblocks-reconfigure-parameters, kubeblocks-switchover,
        │                   kubeblocks-minor-version-upgrade, kubeblocks-expose-service
        │
        ├── Data Protection: kubeblocks-backup, kubeblocks-restore
        │
        ├── Security:       kubeblocks-manage-accounts, kubeblocks-configure-tls
        │
        └── Observability:  kubeblocks-setup-monitoring
```

Generic operation skills (e.g., `kubeblocks-vertical-scaling`) provide universal OpsRequest templates. Engine-specific skills (e.g., `kubeblocks-addon-mysql`) provide topology selection, cluster YAML examples, and connection methods. They cross-reference each other.

## Documentation

- [KubeBlocks Official Docs](https://kubeblocks.io/docs/preview/user_docs/overview/introduction)
- [KubeBlocks GitHub](https://github.com/apecloud/kubeblocks)
- [KubeBlocks LLM Index](https://kubeblocks.io/llms-full.txt)
- [Supported Addons](https://kubeblocks.io/docs/preview/user_docs/overview/supported-addons)

## Contributing

To add a new skill:

1. Create a new directory under the repository root (e.g., `kubeblocks-addon-elasticsearch/`)
2. Add a `SKILL.md` with YAML frontmatter (`name` and `description` fields)
3. Optionally add `reference.md` for detailed supplementary material
4. Update this README's skill tables
5. Update `kubeblocks-overview/SKILL.md` navigation map

## License

[Apache 2.0](LICENSE)
