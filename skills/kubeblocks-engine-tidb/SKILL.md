---
name: kubeblocks-engine-tidb
version: "0.1.0"
description: Primary create-time entry for TiDB on KubeBlocks. Use when the user wants to provision TiDB and needs the correct topology, version, storage, sizing, connection, and next-hop guidance. Run kubeblocks-preflight first when environment readiness is unknown.
---

# TiDB Engine Entry

Use this as the primary create-time entry for TiDB.

## Entry Contract

- Run [kubeblocks-preflight](../kubeblocks-preflight/SKILL.md) whenever storage, scheduling, addon readiness, or observability readiness is still unknown.
- Use [engine-tier-map](../../references/coverage/engine-tier-map.yaml), [addon-capability-matrix](../../references/coverage/addon-capability-matrix.yaml), and [route-matrix](../../references/routing/route-matrix.yaml) as the routing and support truth.
- Keep this entry focused on create-time decisions only: topology, `serviceVersion`, storage and scheduling requirements, sizing, first connection, and next hops.
- Route existing-cluster work to the matching `kubeblocks-op-*` skill and broad monitoring asks to [kubeblocks-observability-router](../kubeblocks-observability-router/SKILL.md).

## Create-Time Checklist

1. Confirm the preflight recommendation bundle, especially `storageClassName`, topology-aware storage risk, and observability mode.
2. Select the engine-specific topology and `serviceVersion`.
3. Choose demo vs production sizing.
4. Decide the first readiness / connection verification step.
5. Hand off follow-up operations to the shared capability layers instead of extending the create path.

## Preserved Detailed Reference

Use [addon-capability-matrix](../../references/coverage/addon-capability-matrix.yaml) and the `example_refs` listed there as the authoritative first-batch references until a full dedicated guide lands.
