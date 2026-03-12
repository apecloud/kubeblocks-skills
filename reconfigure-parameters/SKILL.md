---
name: reconfigure-parameters
description: Modify database configuration parameters for KubeBlocks clusters. Supports dynamic (no restart) and static (requires restart) parameter changes. Use when the user wants to change, tune, or modify database settings or parameters.
---

# Reconfigure Database Parameters

## Overview

KubeBlocks allows modifying database configuration parameters through the `OpsRequest` CR with `type: Reconfiguring`. Parameters are categorized as:

- **Dynamic**: Applied immediately without restart (e.g. `max_connections` for MySQL)
- **Static**: Requires a rolling restart of pods to take effect (e.g. `innodb_buffer_pool_size` for MySQL)

KubeBlocks automatically determines whether a restart is needed based on the parameter type.

Official docs: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/configuration/configure-cluster-parameters

## Workflow

```
- [ ] Step 1: Identify the parameter to change
- [ ] Step 2: Create Reconfiguring OpsRequest
- [ ] Step 3: Verify the change
```

## Step 1: Identify the Parameter

Check current configuration values:

```bash
# List config templates for the cluster
kubectl get configurations -n <ns> -l app.kubernetes.io/instance=<cluster>
```

For a reference of common parameters per addon, see [reference.md](reference.md).

## Step 2: Create Reconfiguring OpsRequest

### Single Parameter Change

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: <cluster>-reconfigure
  namespace: <ns>
spec:
  clusterName: <cluster>
  type: Reconfiguring
  reconfigures:
  - componentName: <component>
    parameters:
    - key: max_connections
      value: "500"
```

### Multiple Parameters

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: <cluster>-reconfigure
  namespace: <ns>
spec:
  clusterName: <cluster>
  type: Reconfiguring
  reconfigures:
  - componentName: <component>
    parameters:
    - key: max_connections
      value: "500"
    - key: innodb_buffer_pool_size
      value: "2147483648"
```

Apply it:

```bash
kubectl apply -f reconfigure-ops.yaml
```

## Step 3: Verify the Change

### Watch OpsRequest Status

```bash
kubectl get ops <cluster>-reconfigure -n <ns> -w
```

Status progression:
- `Pending` → `Running` → `Succeed` (dynamic parameters)
- `Pending` → `Running` → `Restarting` → `Succeed` (static parameters, triggers rolling restart)

### Verify Parameter Value

Connect to the database and check:

```bash
# MySQL
kubectl exec -it <pod> -n <ns> -- mysql -u root -p -e "SHOW VARIABLES LIKE 'max_connections';"

# PostgreSQL
kubectl exec -it <pod> -n <ns> -- psql -U postgres -c "SHOW max_connections;"

# Redis
kubectl exec -it <pod> -n <ns> -- redis-cli CONFIG GET maxmemory
```

## Dynamic vs Static Parameters

| Behavior | Dynamic | Static |
|----------|---------|--------|
| Restart required | No | Yes (rolling restart) |
| Downtime | None | Brief per-pod during rolling restart |
| Effect | Immediate | After pod restart |

KubeBlocks handles the restart automatically for static parameters. Secondary pods restart first, then a switchover occurs, and the original primary restarts last — minimizing downtime.

## Troubleshooting

**OpsRequest fails with validation error:**
- Check that the parameter key exists for the addon
- Verify the value is within the allowed range
- Ensure the component name is correct: `kubectl get cluster <cluster> -n <ns> -o jsonpath='{.spec.componentSpecs[*].name}'`

**Rolling restart takes too long:**
- Static parameter changes trigger sequential pod restarts
- Check pod status: `kubectl get pods -n <ns> -l app.kubernetes.io/instance=<cluster> -w`

## Additional Reference

For a list of common tunable parameters per database addon, see [reference.md](reference.md).
