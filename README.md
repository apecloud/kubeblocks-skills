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
| [create-local-k8s-cluster](./create-local-k8s-cluster/SKILL.md) | Create a local Kubernetes test cluster using Kind, Minikube, or k3d. |
| [install-kubeblocks](./install-kubeblocks/SKILL.md) | Install the KubeBlocks operator. Handles version selection, network detection, registry configuration. |
| [manage-addons](./manage-addons/SKILL.md) | Install, uninstall, and upgrade database engine addons. |

### Cluster Provisioning & Deletion

| Skill | Description |
|-------|-------------|
| [create-cluster](./create-cluster/SKILL.md) | Create a database cluster (generic entry point for all addons). |
| [delete-cluster](./delete-cluster/SKILL.md) | Safely delete a database cluster with pre-deletion checks. |

### Day-2 Operations

| Skill | Description |
|-------|-------------|
| [cluster-lifecycle](./cluster-lifecycle/SKILL.md) | Stop, start, and restart database clusters. |
| [vertical-scaling](./vertical-scaling/SKILL.md) | Scale CPU and memory resources. |
| [horizontal-scaling](./horizontal-scaling/SKILL.md) | Add/remove replicas or shards. |
| [volume-expansion](./volume-expansion/SKILL.md) | Expand persistent volume storage. |
| [reconfigure-parameters](./reconfigure-parameters/SKILL.md) | Modify database configuration parameters. |
| [minor-version-upgrade](./minor-version-upgrade/SKILL.md) | Upgrade database engine minor versions. |
| [switchover](./switchover/SKILL.md) | Perform planned primary-secondary switchover. |
| [expose-service](./expose-service/SKILL.md) | Expose databases externally via LoadBalancer or NodePort. |

### Data Protection

| Skill | Description |
|-------|-------------|
| [backup](./backup/SKILL.md) | Create on-demand, scheduled, and continuous backups. |
| [restore](./restore/SKILL.md) | Restore from backups with full restore or Point-in-Time Recovery. |

### Security

| Skill | Description |
|-------|-------------|
| [manage-accounts](./manage-accounts/SKILL.md) | Manage database passwords and password policies. |
| [configure-tls](./configure-tls/SKILL.md) | Configure TLS, custom certificates, and mTLS. |

### Observability

| Skill | Description |
|-------|-------------|
| [setup-monitoring](./setup-monitoring/SKILL.md) | Set up Prometheus monitoring and Grafana dashboards. |

### Engine-Specific Skills

| Skill | Description |
|-------|-------------|
| [addon-mysql](./addon-mysql/SKILL.md) | MySQL topologies (semi-sync, MGR, Orchestrator, ProxySQL variants). |
| [addon-postgresql](./addon-postgresql/SKILL.md) | PostgreSQL with Patroni-based HA replication. |
| [addon-redis](./addon-redis/SKILL.md) | Redis standalone, replication with Sentinel, and Redis Cluster sharding. |
| [addon-mongodb](./addon-mongodb/SKILL.md) | MongoDB ReplicaSet and Sharding topologies. |
| [addon-kafka](./addon-kafka/SKILL.md) | Apache Kafka combined and separated broker/controller modes. |

## How to Use

### Cursor

Copy or symlink skill directories into your Cursor skills folder:

```bash
# Personal skills (available across all projects)
cp -r kubeblocks-overview ~/.cursor/skills/
cp -r install-kubeblocks ~/.cursor/skills/
# ... repeat for desired skills

# Or clone the whole repo and symlink
ln -s /path/to/kubeblocks-skills/kubeblocks-overview ~/.cursor/skills/kubeblocks-overview
```

### Claude Code

Reference skill files when prompting:

```
Read kubeblocks-overview/SKILL.md and help me deploy a MySQL cluster.
```

### Other Agents

Point the agent to the `SKILL.md` file in the relevant skill directory. All instructions are in standard markdown and agent-agnostic.

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
        ├── Infrastructure: create-local-k8s-cluster → install-kubeblocks → manage-addons
        │
        ├── Provisioning:   create-cluster ←→ addon-{mysql,pg,redis,mongodb,kafka}
        │                   delete-cluster
        │
        ├── Operations:     cluster-lifecycle, vertical-scaling, horizontal-scaling,
        │                   volume-expansion, reconfigure-parameters, switchover,
        │                   minor-version-upgrade, expose-service
        │
        ├── Data Protection: backup, restore
        │
        ├── Security:       manage-accounts, configure-tls
        │
        └── Observability:  setup-monitoring
```

Generic operation skills (e.g., `vertical-scaling`) provide universal OpsRequest templates. Engine-specific skills (e.g., `addon-mysql`) provide topology selection, cluster YAML examples, and connection methods. They cross-reference each other.

## Documentation

- [KubeBlocks Official Docs](https://kubeblocks.io/docs/preview/user_docs/overview/introduction)
- [KubeBlocks GitHub](https://github.com/apecloud/kubeblocks)
- [KubeBlocks LLM Index](https://kubeblocks.io/llms-full.txt)
- [Supported Addons](https://kubeblocks.io/docs/preview/user_docs/overview/supported-addons)

## Contributing

To add a new skill:

1. Create a new directory under the repository root (e.g., `addon-elasticsearch/`)
2. Add a `SKILL.md` with YAML frontmatter (`name` and `description` fields)
3. Optionally add `reference.md` for detailed supplementary material
4. Update this README's skill tables
5. Update `kubeblocks-overview/SKILL.md` navigation map

## License

[Apache 2.0](LICENSE)
