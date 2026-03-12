---
name: kubeblocks-overview
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
| Install KubeBlocks operator | [install-kubeblocks](../install-kubeblocks/SKILL.md) | `install-kubeblocks/SKILL.md` |
| Create a local K8s test cluster | [create-local-k8s-cluster](../create-local-k8s-cluster/SKILL.md) | `create-local-k8s-cluster/SKILL.md` |
| Install/manage database addons | [manage-addons](../manage-addons/SKILL.md) | `manage-addons/SKILL.md` |

### Cluster Provisioning & Deletion

| User Intent | Skill | Path |
|---|---|---|
| Create a database cluster (generic) | [create-cluster](../create-cluster/SKILL.md) | `create-cluster/SKILL.md` |
| Create a MySQL cluster | [addon-mysql](../addon-mysql/SKILL.md) | `addon-mysql/SKILL.md` |
| Create a PostgreSQL cluster | [addon-postgresql](../addon-postgresql/SKILL.md) | `addon-postgresql/SKILL.md` |
| Create a Redis cluster | [addon-redis](../addon-redis/SKILL.md) | `addon-redis/SKILL.md` |
| Create a MongoDB cluster | [addon-mongodb](../addon-mongodb/SKILL.md) | `addon-mongodb/SKILL.md` |
| Create a Kafka cluster | [addon-kafka](../addon-kafka/SKILL.md) | `addon-kafka/SKILL.md` |
| Create an Elasticsearch cluster | [addon-elasticsearch](../addon-elasticsearch/SKILL.md) | `addon-elasticsearch/SKILL.md` |
| Create a Milvus (vector DB) cluster | [addon-milvus](../addon-milvus/SKILL.md) | `addon-milvus/SKILL.md` |
| Create a Qdrant (vector DB) cluster | [addon-qdrant](../addon-qdrant/SKILL.md) | `addon-qdrant/SKILL.md` |
| Create a RabbitMQ cluster | [addon-rabbitmq](../addon-rabbitmq/SKILL.md) | `addon-rabbitmq/SKILL.md` |
| Delete a database cluster | [delete-cluster](../delete-cluster/SKILL.md) | `delete-cluster/SKILL.md` |

### Day-2 Operations

| User Intent | Skill | Path |
|---|---|---|
| Stop / Start / Restart a cluster | [cluster-lifecycle](../cluster-lifecycle/SKILL.md) | `cluster-lifecycle/SKILL.md` |
| Scale CPU / Memory (vertical) | [vertical-scaling](../vertical-scaling/SKILL.md) | `vertical-scaling/SKILL.md` |
| Add / remove replicas or shards | [horizontal-scaling](../horizontal-scaling/SKILL.md) | `horizontal-scaling/SKILL.md` |
| Expand storage volume | [volume-expansion](../volume-expansion/SKILL.md) | `volume-expansion/SKILL.md` |
| Change database parameters | [reconfigure-parameters](../reconfigure-parameters/SKILL.md) | `reconfigure-parameters/SKILL.md` |
| Primary / secondary switchover | [switchover](../switchover/SKILL.md) | `switchover/SKILL.md` |
| Upgrade database engine version | [minor-version-upgrade](../minor-version-upgrade/SKILL.md) | `minor-version-upgrade/SKILL.md` |
| Rebuild a failed replica | [rebuild-replica](../rebuild-replica/SKILL.md) | `rebuild-replica/SKILL.md` |
| Upgrade KubeBlocks operator | [upgrade-kubeblocks](../upgrade-kubeblocks/SKILL.md) | `upgrade-kubeblocks/SKILL.md` |

### Data Protection

| User Intent | Skill | Path |
|---|---|---|
| Backup cluster data | [backup](../backup/SKILL.md) | `backup/SKILL.md` |
| Restore from backup / PITR | [restore](../restore/SKILL.md) | `restore/SKILL.md` |

### Security & Networking

| User Intent | Skill | Path |
|---|---|---|
| Manage database passwords / accounts | [manage-accounts](../manage-accounts/SKILL.md) | `manage-accounts/SKILL.md` |
| Configure TLS / mTLS encryption | [configure-tls](../configure-tls/SKILL.md) | `configure-tls/SKILL.md` |
| Expose service externally (LoadBalancer/NodePort) | [expose-service](../expose-service/SKILL.md) | `expose-service/SKILL.md` |

### Observability

| User Intent | Skill | Path |
|---|---|---|
| Setup monitoring (Prometheus/Grafana) | [setup-monitoring](../setup-monitoring/SKILL.md) | `setup-monitoring/SKILL.md` |

### Troubleshooting

| User Intent | Skill | Path |
|---|---|---|
| Cluster not working, error, failed, stuck, CrashLoopBackOff, diagnose | [troubleshoot](../troubleshoot/SKILL.md) | `troubleshoot/SKILL.md` |

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
