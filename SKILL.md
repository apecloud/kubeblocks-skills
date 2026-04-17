---
name: kubeblocks
version: "0.3.0"
description: Route database work on Kubernetes to the right KubeBlocks skill. Use this as the top-level entrypoint when the user needs a database, database operations, or database observability on Kubernetes. The root skill only decides the next hop; detailed workflows live in the leaf skills.
compatibility:
  required_tools:
    - kubectl
    - helm
  optional_tools:
    - npx
  notes: Requires Kubernetes access for install, preflight, provisioning, and operations. For local development, create a cluster first.
---

# KubeBlocks Router

This root skill is a **router only**. It should decide the next step, not re-explain every workflow.

Use [README.md](README.md) for repository overview, installation instructions, and the full skill catalog.

## Route Order

Always route in this order:

1. **No Kubernetes cluster yet**
   Route to [create-local-k8s-cluster](skills/kubeblocks-create-local-k8s-cluster/SKILL.md).

2. **Kubernetes exists, but KubeBlocks is not installed**
   Route to [install-kubeblocks](skills/kubeblocks-install/SKILL.md).

3. **First-time provisioning, or environment readiness is unknown**
   Route to [kubeblocks-preflight](skills/kubeblocks-preflight/SKILL.md) before any engine-specific provisioning.

4. **Provision a database after preflight**
   - MySQL → [addon-mysql](skills/kubeblocks-addon-mysql/SKILL.md)
   - PostgreSQL → [addon-postgresql](skills/kubeblocks-addon-postgresql/SKILL.md)
   - Redis → [addon-redis](skills/kubeblocks-addon-redis/SKILL.md)
   - MongoDB → [addon-mongodb](skills/kubeblocks-addon-mongodb/SKILL.md)
   - Kafka → [addon-kafka](skills/kubeblocks-addon-kafka/SKILL.md)
   - Elasticsearch → [addon-elasticsearch](skills/kubeblocks-addon-elasticsearch/SKILL.md)
   - Milvus → [addon-milvus](skills/kubeblocks-addon-milvus/SKILL.md)
   - Qdrant → [addon-qdrant](skills/kubeblocks-addon-qdrant/SKILL.md)
   - RabbitMQ → [addon-rabbitmq](skills/kubeblocks-addon-rabbitmq/SKILL.md)
   - Other engines without dedicated entry skills → [create-cluster](skills/kubeblocks-create-cluster/SKILL.md)

5. **Operate an existing cluster**
   Route to the matching Day-2 skill:
   - lifecycle, scaling, backup, restore, parameters, switchover, rebuild, expose, TLS, accounts, or upgrade.

6. **Observability**
   - Existing Prometheus/Grafana stack → [observability-existing-stack](skills/kubeblocks-observability-existing-stack/SKILL.md)
   - No monitoring base yet → [observability-bootstrap-stack](skills/kubeblocks-observability-bootstrap-stack/SKILL.md)
   - If the user only says “set up monitoring”, use the shim [setup-monitoring](skills/kubeblocks-setup-monitoring/SKILL.md), which routes to the right observability branch.

7. **Troubleshooting**
   Route to [troubleshoot](skills/kubeblocks-troubleshoot/SKILL.md).

## Hard Routing Rules

- Do **not** route MySQL, PostgreSQL, Redis, MongoDB, or Kafka to the generic [create-cluster](skills/kubeblocks-create-cluster/SKILL.md) path.
- Do **not** provision a first-time database without going through [kubeblocks-preflight](skills/kubeblocks-preflight/SKILL.md) when environment readiness is unknown.
- Do **not** equate “metrics exist” with “monitoring is delivered”. Observability must declare whether it is only `metrics-ready`, `scrape-ready`, `dashboard-ready`, or `alerting-ready`.

## Recommendation Bundle Contract

[kubeblocks-preflight](skills/kubeblocks-preflight/SKILL.md) should produce an environment profile / recommendation bundle that downstream engine-entry skills can consume. At minimum it must answer:

- Recommended `storageClassName`
- Whether topology-aware / `WaitForFirstConsumer` storage is required
- Which engine entry skill to use
- Which generic paths are forbidden
- Demo vs production sizing guidance
- Whether observability should go to `existing-stack` or `bootstrap-stack`

## Common Misroutes To Prevent

- **ACK multi-AZ + PostgreSQL/MySQL**:
  Route to `preflight` first. Do not jump directly from install to addon provisioning.
- **Existing Prometheus/Grafana**:
  Route to `observability-existing-stack`, not full monitoring bootstrap.
- **Unknown or low-frequency engines**:
  Only then use [create-cluster](skills/kubeblocks-create-cluster/SKILL.md) as the `other-addons` fallback.
