# Scenario Matrix

| Scenario | Input Conditions | Expected Route | Prohibited Route | Notes |
|---|---|---|---|---|
| ACK multi-AZ + PostgreSQL | KubeBlocks installed, multi-AZ storage unknown | `kubeblocks-preflight` -> `kubeblocks-addon-postgresql` | `kubeblocks-create-cluster` | Storage and topology must be decided first |
| ACK multi-AZ + MySQL | KubeBlocks installed, storage class may bind immediately | `kubeblocks-preflight` -> `kubeblocks-addon-mysql` | `kubeblocks-create-cluster` | Avoid PVC/node-affinity traps |
| Existing Prometheus / Grafana | Exporter present, monitoring base already exists | `kubeblocks-observability-existing-stack` | `kubeblocks-observability-bootstrap-stack` | Integration, not bootstrap |
| Unknown engine | No dedicated engine-entry skill | `kubeblocks-create-cluster` | High-frequency addon entry mismatch | This is the only case where generic fallback is valid |
