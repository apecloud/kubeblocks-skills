# KubeBlocks Skills V2 Structure Plan

This document fixes the V2 rewrite direction before large-scale content edits begin.

## Goals

1. Cover the KubeBlocks capability surface more completely across engines and Day-2 operations.
2. Separate executable skills from facts, fixtures, and validators.
3. Make route drift, addon coverage drift, and ops coverage drift machine-detectable.
4. Keep V1 skill names alive as shims until V2 routing is stable.

## Final Acceptance Standard

The target is not "a prettier directory tree." The target is:

> A single agent with only `kubeblocks-skills` should be able to safely choose
> the next step, provision the right engine path, and operate supported Day-2
> actions without hidden tribal knowledge.

That standard forces four first-principles constraints:

1. Routing must be deterministic.
2. Preflight must resolve environment risk before create-time guidance.
3. Engine entry must close the create-time decision loop for that engine.
4. Supported Day-2 and observability actions must come from data truth, not prose.

## Hard Rules

- Real executable skills live only under `skills/`.
- `references/coverage`, `references/routing`, and `references/testing` are the single sources of truth.
- `tests/fixtures` contains machine-runnable cases only.
- `scripts/` validates repo consistency against those facts; scripts must not invent a second truth.
- Tier is expressed in coverage matrices, not in directory depth.

## V2 Skill Taxonomy

- Root router: `kubeblocks`
- Environment gate: `kubeblocks-install`, `kubeblocks-create-local-k8s-cluster`, `kubeblocks-preflight`
- Dedicated engine entry: `kubeblocks-engine-*`
- Family-backed guidance: reference-only taxonomy in coverage and routing facts
- Generic fallback: `kubeblocks-engine-generic`
- Day-2 operations: `kubeblocks-op-*`
- Observability: `kubeblocks-observability-*`
- Troubleshoot / recovery: `kubeblocks-troubleshoot`, `kubeblocks-rebuild-replica`

## Coverage Model

### Tier 1: Dedicated engine entry required

- mysql
- postgresql
- redis
- mongodb
- kafka
- elasticsearch
- milvus
- qdrant
- rabbitmq
- clickhouse
- mariadb
- minio
- opensearch
- pulsar
- tidb

### Tier 2: Family-backed first

- etcd
- zookeeper
- victoria-metrics
- loki
- greptimedb
- risingwave
- falkordb
- influxdb
- weaviate
- starrocks-ce
- oceanbase-ce
- nebula
- neo4j

### Tier 3: Generic or vendor-specialized first

- apecloud-mysql
- apecloud-mysql-cluster
- etcd-cluster
- mogdb
- orioledb
- polardbx
- rocketmq
- vanilla-postgresql
- xinference
- yashandb
- neon
- orchestrator
- llm
- kblib

## Four Single Sources Of Truth

1. `references/coverage/engine-tier-map.yaml`
2. `references/coverage/addon-capability-matrix.yaml`
3. `references/coverage/ops-capability-matrix.yaml`
4. `references/routing/route-matrix.yaml`

Schema files define the contract, but they are not the data truth:

- `references/coverage/addon-capability-matrix.schema.yaml`
- `references/coverage/ops-capability-matrix.schema.yaml`
- `references/routing/route-matrix.schema.yaml`

The human-readable routing and migration guidance then hangs off:

- `references/routing/*.md`
- `references/testing/path-migrations.md`
- `references/testing/scenario-matrix.md`
- `references/testing/smoke-checklist.md`

## Compatibility Strategy

V2 does not hard-delete V1 names in the first PR.

Examples:

- `kubeblocks-addon-mysql` -> shim to `kubeblocks-engine-mysql`
- `kubeblocks-create-cluster` -> shim to `kubeblocks-engine-generic`
- `kubeblocks-setup-monitoring` -> shim to `kubeblocks-observability-router`
- existing Day-2 skills stay visible while routing and documentation move toward `kubeblocks-op-*`

## Initial Deliverables For The Next PR

1. V2 structure planning facts and schemas
2. Tier-1 engine map
3. Shim mapping fixtures
4. Tier-1 routing/coverage fixtures
5. Starter data-truth files for addon, ops, and routing matrices
6. Drift-check skeletons for addon coverage, ops coverage, and routing
