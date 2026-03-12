---
name: switchover
description: Perform planned primary-secondary switchover for KubeBlocks database clusters via OpsRequest. Promotes a replica to primary with minimal downtime. Use when the user wants to promote a replica, switch primary, change leader, perform a planned failover, or do maintenance on the current primary node. NOT for unplanned failover recovery (handled automatically by HA middleware like Patroni, Orchestrator, or Sentinel) or restarting all pods (see cluster-lifecycle).
---

# Switchover Primary-Secondary

## Overview

A switchover is a **planned** operation that promotes a secondary replica to primary and demotes the current primary to secondary. This is useful for maintenance, load rebalancing, or pre-failover testing.

Switchover is only available for addons with primary/secondary replication roles:
- MySQL / ApeCloud MySQL
- PostgreSQL
- Redis (replication mode)
- MongoDB (replica set)

Official docs: https://kubeblocks.io/docs/preview/user_docs/handle-an-exception/switchover

## Workflow

```
- [ ] Step 1: Check current roles
- [ ] Step 2: Perform switchover via OpsRequest
- [ ] Step 3: Verify new roles
```

## Step 1: Check Current Roles

Identify which pod is the current primary:

```bash
kubectl get pods -n <ns> -l app.kubernetes.io/instance=<cluster> \
  -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.labels.kubeblocks\.io/role}{"\n"}{end}'
```

Example output:

```
mycluster-mysql-0    primary
mycluster-mysql-1    secondary
mycluster-mysql-2    secondary
```

## Step 2: Perform Switchover

### Switchover via OpsRequest

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: <cluster>-switchover
  namespace: <ns>
spec:
  clusterName: <cluster>
  type: Switchover
  switchover:
  - componentName: <component>
    instanceName: <current-primary-pod>
```

- `componentName`: the component name from the Cluster spec (e.g. `mysql`, `postgresql`)
- `instanceName`: the pod name of the **current primary** that should be demoted

Apply it:

```bash
kubectl apply -f switchover-ops.yaml
kubectl get ops <cluster>-switchover -n <ns> -w
```

Status will progress: `Pending` → `Running` → `Succeed`

## Step 3: Verify New Roles

After the OpsRequest succeeds, confirm the roles have changed:

```bash
kubectl get pods -n <ns> -l app.kubernetes.io/instance=<cluster> \
  -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.labels.kubeblocks\.io/role}{"\n"}{end}'
```

Expected: a different pod should now have the `primary` role.

Also verify replication health:

```bash
# MySQL: check replication status
kubectl exec -it <new-secondary-pod> -n <ns> -- mysql -u root -p -e "SHOW REPLICA STATUS\G"

# PostgreSQL: check replication
kubectl exec -it <primary-pod> -n <ns> -- psql -U postgres -c "SELECT * FROM pg_stat_replication;"
```

## Important Notes

- Switchover is a **planned** operation, not a failover. The current primary must be healthy and reachable.
- During switchover, there is a brief period where writes are unavailable (typically seconds).
- Client connections to the primary service are automatically re-routed after switchover completes.
- KubeBlocks uses the HA proxy or service endpoint to ensure clients connect to the new primary.

## Troubleshooting

**Switchover OpsRequest fails:**
- Ensure the cluster has more than one replica
- Verify the current primary pod name is correct
- Check that all pods are in Running state before switchover

**Roles not updated after switchover:**
- Wait a few seconds for label propagation
- Check OpsRequest events: `kubectl describe ops <name> -n <ns>`

**Replication lag after switchover:**
- The new secondary (former primary) may need time to catch up
- Monitor with: `kubectl exec -it <pod> -n <ns> -- <db-specific-replication-check>`
