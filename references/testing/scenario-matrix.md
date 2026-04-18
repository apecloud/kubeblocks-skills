# Scenario Matrix

| Scenario | Input Conditions | Expected Route | Prohibited Route | Notes |
|---|---|---|---|---|
| ACK multi-AZ + PostgreSQL | KubeBlocks installed, multi-AZ storage unknown | `kubeblocks-preflight` -> `kubeblocks-engine-postgresql` | `kubeblocks-engine-generic` | Storage and topology must be decided first |
| ACK multi-AZ + MySQL | KubeBlocks installed, storage class may bind immediately | `kubeblocks-preflight` -> `kubeblocks-engine-mysql` | `kubeblocks-engine-generic` | Avoid PVC/node-affinity traps |
| Existing Prometheus / Grafana | Exporter present, monitoring base already exists | `kubeblocks-observability-existing-stack` | `kubeblocks-observability-bootstrap-stack` | Integration, not bootstrap |
| Unknown engine | No dedicated engine-entry skill | `kubeblocks-engine-generic` | Tier-1 dedicated engine entry mismatch | This is the only case where generic fallback is valid |
| Legacy skill name still used | User or agent calls `kubeblocks-addon-*` or an old Day-2 name | shim -> new engine/op entry | old name treated as primary route | Compatibility must not restore the old main path |
