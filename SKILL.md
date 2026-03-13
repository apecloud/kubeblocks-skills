---
name: kubeblocks-overview
version: "0.1.0"
description: Navigate KubeBlocks capabilities and route to the right skill for any database management task. Use when the user asks about KubeBlocks features, wants to manage databases on Kubernetes, or needs guidance on which operation to perform. Also use as an entry point when the intent is unclear. NOT a skill that performs actions itself — it identifies and delegates to the appropriate skill.
---

# KubeBlocks Skills Navigator

## What is KubeBlocks?

KubeBlocks is a Kubernetes operator that manages 30+ database engines on any K8s cluster. It provides a unified API for the full lifecycle of databases — from provisioning and scaling to backup, restore, and observability — across relational, NoSQL, streaming, vector, time-series, and graph databases.

- Official docs: https://kubeblocks.io/docs/preview/user_docs/overview/introduction
- Full LLM doc index: https://kubeblocks.io/llms-full.txt
- GitHub: https://github.com/apecloud/kubeblocks

## Quick Status Check

Before performing any operation, verify the current state:

```bash
# Check KubeBlocks operator health
kubectl -n kb-system get pods

# List all database clusters across namespaces
kubectl get cluster -A

# Check KubeBlocks version
helm list -n kb-system | grep kubeblocks
```

## Skill Map

Use the table below to find the right skill for any task.

### Setup & Infrastructure

| User Intent | Skill | Path |
|---|---|---|
| Install KubeBlocks operator | [install-kubeblocks](skills/kubeblocks-install/SKILL.md) | `skills/kubeblocks-install/SKILL.md` |
| Create a local K8s test cluster | [create-local-k8s-cluster](skills/kubeblocks-create-local-k8s-cluster/SKILL.md) | `skills/kubeblocks-create-local-k8s-cluster/SKILL.md` |
| Install/manage database addons | [manage-addons](skills/kubeblocks-manage-addons/SKILL.md) | `skills/kubeblocks-manage-addons/SKILL.md` |

### Cluster Provisioning & Deletion

| User Intent | Skill | Path |
|---|---|---|
| Create a database cluster (generic) | [create-cluster](skills/kubeblocks-create-cluster/SKILL.md) | `skills/kubeblocks-create-cluster/SKILL.md` |
| Create a MySQL cluster | [addon-mysql](skills/kubeblocks-addon-mysql/SKILL.md) | `skills/kubeblocks-addon-mysql/SKILL.md` |
| Create a PostgreSQL cluster | [addon-postgresql](skills/kubeblocks-addon-postgresql/SKILL.md) | `skills/kubeblocks-addon-postgresql/SKILL.md` |
| Create a Redis cluster | [addon-redis](skills/kubeblocks-addon-redis/SKILL.md) | `skills/kubeblocks-addon-redis/SKILL.md` |
| Create a MongoDB cluster | [addon-mongodb](skills/kubeblocks-addon-mongodb/SKILL.md) | `skills/kubeblocks-addon-mongodb/SKILL.md` |
| Create a Kafka cluster | [addon-kafka](skills/kubeblocks-addon-kafka/SKILL.md) | `skills/kubeblocks-addon-kafka/SKILL.md` |
| Create an Elasticsearch cluster | [addon-elasticsearch](skills/kubeblocks-addon-elasticsearch/SKILL.md) | `skills/kubeblocks-addon-elasticsearch/SKILL.md` |
| Create a Milvus (vector DB) cluster | [addon-milvus](skills/kubeblocks-addon-milvus/SKILL.md) | `skills/kubeblocks-addon-milvus/SKILL.md` |
| Create a Qdrant (vector DB) cluster | [addon-qdrant](skills/kubeblocks-addon-qdrant/SKILL.md) | `skills/kubeblocks-addon-qdrant/SKILL.md` |
| Create a RabbitMQ cluster | [addon-rabbitmq](skills/kubeblocks-addon-rabbitmq/SKILL.md) | `skills/kubeblocks-addon-rabbitmq/SKILL.md` |
| Delete a database cluster | [delete-cluster](skills/kubeblocks-delete-cluster/SKILL.md) | `skills/kubeblocks-delete-cluster/SKILL.md` |

### Day-2 Operations

| User Intent | Skill | Path |
|---|---|---|
| Stop / Start / Restart a cluster | [cluster-lifecycle](skills/kubeblocks-cluster-lifecycle/SKILL.md) | `skills/kubeblocks-cluster-lifecycle/SKILL.md` |
| Scale CPU / Memory (vertical) | [vertical-scaling](skills/kubeblocks-vertical-scaling/SKILL.md) | `skills/kubeblocks-vertical-scaling/SKILL.md` |
| Add / remove replicas or shards | [horizontal-scaling](skills/kubeblocks-horizontal-scaling/SKILL.md) | `skills/kubeblocks-horizontal-scaling/SKILL.md` |
| Expand storage volume | [volume-expansion](skills/kubeblocks-volume-expansion/SKILL.md) | `skills/kubeblocks-volume-expansion/SKILL.md` |
| Change database parameters | [reconfigure-parameters](skills/kubeblocks-reconfigure-parameters/SKILL.md) | `skills/kubeblocks-reconfigure-parameters/SKILL.md` |
| Primary / secondary switchover | [switchover](skills/kubeblocks-switchover/SKILL.md) | `skills/kubeblocks-switchover/SKILL.md` |
| Upgrade database engine version | [minor-version-upgrade](skills/kubeblocks-minor-version-upgrade/SKILL.md) | `skills/kubeblocks-minor-version-upgrade/SKILL.md` |
| Rebuild a failed replica | [rebuild-replica](skills/kubeblocks-rebuild-replica/SKILL.md) | `skills/kubeblocks-rebuild-replica/SKILL.md` |
| Upgrade KubeBlocks operator | [upgrade-kubeblocks](skills/kubeblocks-upgrade/SKILL.md) | `skills/kubeblocks-upgrade/SKILL.md` |

### Data Protection

| User Intent | Skill | Path |
|---|---|---|
| Backup cluster data | [backup](skills/kubeblocks-backup/SKILL.md) | `skills/kubeblocks-backup/SKILL.md` |
| Restore from backup / PITR | [restore](skills/kubeblocks-restore/SKILL.md) | `skills/kubeblocks-restore/SKILL.md` |

### Security & Networking

| User Intent | Skill | Path |
|---|---|---|
| Manage database passwords / accounts | [manage-accounts](skills/kubeblocks-manage-accounts/SKILL.md) | `skills/kubeblocks-manage-accounts/SKILL.md` |
| Configure TLS / mTLS encryption | [configure-tls](skills/kubeblocks-configure-tls/SKILL.md) | `skills/kubeblocks-configure-tls/SKILL.md` |
| Expose service externally (LoadBalancer/NodePort) | [expose-service](skills/kubeblocks-expose-service/SKILL.md) | `skills/kubeblocks-expose-service/SKILL.md` |

### Observability

| User Intent | Skill | Path |
|---|---|---|
| Setup monitoring (Prometheus/Grafana) | [setup-monitoring](skills/kubeblocks-setup-monitoring/SKILL.md) | `skills/kubeblocks-setup-monitoring/SKILL.md` |

### Troubleshooting

| User Intent | Skill | Path |
|---|---|---|
| Cluster not working, error, failed, stuck, CrashLoopBackOff, diagnose | [troubleshoot](skills/kubeblocks-troubleshoot/SKILL.md) | `skills/kubeblocks-troubleshoot/SKILL.md` |

## Decision Tree

Use this flowchart when the user's intent is unclear:

```
Is KubeBlocks installed?
├─ No  → Do they have a K8s cluster?
│        ├─ No  → create-local-k8s-cluster → install-kubeblocks
│        └─ Yes → install-kubeblocks
└─ Yes → What do they want to do?
         ├─ Create a database     → Is the engine addon installed?
         │                          ├─ No  → manage-addons → then create cluster
         │                          └─ Yes → Is it MySQL/PG/Redis/MongoDB/Kafka/ES/Milvus/Qdrant/RabbitMQ?
         │                                   ├─ Yes → addon-{engine} (topology guidance)
         │                                   └─ No  → create-cluster (generic template)
         ├─ Delete permanently    → delete-cluster
         ├─ Stop temporarily      → cluster-lifecycle (stop, preserves PVCs)
         ├─ Start / Restart       → cluster-lifecycle
         ├─ Scale CPU/Memory      → vertical-scaling
         ├─ Add/remove replicas   → horizontal-scaling
         ├─ Add/remove shards     → horizontal-scaling (shard scaling)
         ├─ Expand disk           → volume-expansion
         ├─ Backup data           → backup
         ├─ Restore from backup   → restore
         ├─ Change DB config      → reconfigure-parameters
         ├─ Switchover primary    → switchover
         ├─ Upgrade DB version    → minor-version-upgrade
         ├─ Rebuild failed replica → rebuild-replica
         ├─ Upgrade KubeBlocks    → upgrade-kubeblocks
         ├─ Manage passwords      → manage-accounts
         ├─ Enable TLS/SSL        → configure-tls
         ├─ Expose externally     → expose-service
         ├─ Setup monitoring      → setup-monitoring
         └─ Cluster error/failed/stuck → troubleshoot
```

## Disambiguation Guide

### create-cluster vs addon-* skills

- Use **addon-mysql**, **addon-postgresql**, **addon-redis**, **addon-mongodb**, **addon-kafka**, **addon-elasticsearch**, **addon-milvus**, **addon-qdrant**, or **addon-rabbitmq** when the user explicitly names one of these engines. These skills include engine-specific topology options, best-practice defaults, and connection instructions.
- Use **create-cluster** for any engine not listed above (ClickHouse, etc.), or when the user wants a general guide that works across all supported databases.

### "Scale" ambiguity

| User says | Skill |
|-----------|-------|
| "scale up", "more CPU", "more memory", "resize" | vertical-scaling |
| "add replicas", "more nodes", "scale out", "add shards" | horizontal-scaling |
| "more disk", "more storage", "expand volume" | volume-expansion |

### "Delete" vs "Stop"

| User says | Skill |
|-----------|-------|
| "delete", "remove", "destroy", "drop" (permanent) | delete-cluster |
| "stop", "pause", "shut down" (temporary, keeps data) | cluster-lifecycle |

### "Upgrade" ambiguity

| User says | Skill |
|-----------|-------|
| "upgrade MySQL/PG version", "patch database" | minor-version-upgrade |
| "upgrade KubeBlocks", "update operator" | upgrade-kubeblocks |

## Safety Patterns

Before performing any cluster-modifying operation, review the [safety-patterns](references/safety-patterns.md) reference for dry-run requirements, status confirmation conventions, and production cluster protection rules.

## Common Debugging Commands

```bash
# Describe a specific cluster
kubectl describe cluster <cluster-name> -n <namespace>

# Check OpsRequest status (scaling, restart, upgrade, etc.)
kubectl get opsrequest -n <namespace>

# View cluster component status
kubectl get component -n <namespace>

# Check pod logs for a cluster
kubectl logs -n <namespace> <pod-name> -c <container-name>

# View KubeBlocks operator logs
kubectl -n kb-system logs -l app.kubernetes.io/name=kubeblocks --tail=100
```

## Documentation Links

| Resource | URL |
|---|---|
| Introduction | https://kubeblocks.io/docs/preview/user_docs/overview/introduction |
| Supported Addons | https://kubeblocks.io/docs/preview/user_docs/overview/supported-addons |
| Full LLM Index | https://kubeblocks.io/llms-full.txt |
| GitHub Repository | https://github.com/apecloud/kubeblocks |
| Releases | https://github.com/apecloud/kubeblocks/releases |
