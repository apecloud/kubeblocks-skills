---
name: horizontal-scaling
description: Scale database cluster replicas or shards horizontally with KubeBlocks. Supports scale-out and scale-in for all addons including sharding topologies. Use when the user wants to add or remove replicas, nodes, or shards.
---

# Horizontal Scaling: Add or Remove Replicas and Shards

## Overview

Horizontal scaling changes the number of replicas (or shards) in a KubeBlocks database cluster. KubeBlocks supports scale-out (add replicas) and scale-in (remove replicas), including decommissioning specific instances and adjusting shard counts for sharded clusters (Redis Cluster, MongoDB sharded).

Official docs: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/scale-a-mysql-cluster
Full doc index: https://kubeblocks.io/llms-full.txt

## Workflow

```
- [ ] Step 1: Check current replicas
- [ ] Step 2: Apply horizontal scaling OpsRequest
- [ ] Step 3: Monitor the operation
- [ ] Step 4: Verify new topology
```

## Step 1: Check Current Replicas

```bash
kubectl get cluster <cluster-name> -n <namespace> -o yaml | grep replicas
```

Or list pods:

```bash
kubectl get pods -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

## Step 2: Apply Horizontal Scaling OpsRequest

### Scale Out (Add Replicas)

```yaml
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: scaleout-<cluster-name>
  namespace: <namespace>
spec:
  clusterName: <cluster-name>
  type: HorizontalScaling
  horizontalScaling:
    - componentName: <component-name>
      scaleOut:
        replicaChanges: <number-to-add>
```

Example — add 2 replicas to a MySQL cluster:

```bash
kubectl apply -f - <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: scaleout-mysql-cluster
  namespace: default
spec:
  clusterName: mysql-cluster
  type: HorizontalScaling
  horizontalScaling:
    - componentName: mysql
      scaleOut:
        replicaChanges: 2
EOF
```

### Scale In (Remove Replicas)

```yaml
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: scalein-<cluster-name>
  namespace: <namespace>
spec:
  clusterName: <cluster-name>
  type: HorizontalScaling
  horizontalScaling:
    - componentName: <component-name>
      scaleIn:
        replicaChanges: <number-to-remove>
```

Example — remove 1 replica from a PostgreSQL cluster:

```bash
kubectl apply -f - <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: scalein-pg-cluster
  namespace: default
spec:
  clusterName: pg-cluster
  type: HorizontalScaling
  horizontalScaling:
    - componentName: postgresql
      scaleIn:
        replicaChanges: 1
EOF
```

### Decommission Specific Instances (Scale In by Name)

To remove a specific pod instead of the last one, use `onlineInstancesToOffline`:

```yaml
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: scalein-specific-<cluster-name>
  namespace: <namespace>
spec:
  clusterName: <cluster-name>
  type: HorizontalScaling
  horizontalScaling:
    - componentName: <component-name>
      scaleIn:
        replicaChanges: 1
        onlineInstancesToOffline:
          - "<pod-name>"
```

Example — decommission a specific MongoDB replica:

```bash
kubectl apply -f - <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: scalein-specific-mongo
  namespace: default
spec:
  clusterName: mongo-cluster
  type: HorizontalScaling
  horizontalScaling:
    - componentName: mongodb
      scaleIn:
        replicaChanges: 1
        onlineInstancesToOffline:
          - "mongo-cluster-mongodb-2"
EOF
```

### Shard Scaling (Redis Cluster / MongoDB Sharded)

For sharded topologies, use the `shards` field to change the number of shard groups:

```yaml
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: scale-shards-<cluster-name>
  namespace: <namespace>
spec:
  clusterName: <cluster-name>
  type: HorizontalScaling
  horizontalScaling:
    - componentName: <component-name>
      scaleOut:
        replicaChanges: <shards-to-add>
```

> **Note:** For Redis Cluster and MongoDB sharded topologies, each "replica" in the component represents a shard group. Increasing replicas adds new shards and triggers data rebalancing automatically.

### kubectl Patch Alternative

For simple replica count changes, you can also patch the cluster directly:

```bash
kubectl patch cluster <cluster-name> -n <namespace> \
  --type merge -p '{"spec":{"componentSpecs":[{"name":"<component-name>","replicas":<new-total>}]}}'
```

Example — set MySQL replicas to 5:

```bash
kubectl patch cluster mysql-cluster -n default \
  --type merge -p '{"spec":{"componentSpecs":[{"name":"mysql","replicas":5}]}}'
```

## Step 3: Monitor the Operation

```bash
kubectl get ops -n <namespace> -w
```

Expected progression: `Pending` → `Running` → `Succeed`.

Watch pods:

```bash
kubectl get pods -n <namespace> -l app.kubernetes.io/instance=<cluster-name> -w
```

## Step 4: Verify New Topology

```bash
kubectl get cluster <cluster-name> -n <namespace> -o yaml | grep replicas
```

Confirm pod count:

```bash
kubectl get pods -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

## Troubleshooting

**Scale-out pods stuck in `Pending`:**
- Insufficient node resources. Check: `kubectl describe pod <pod-name> -n <namespace>`
- Insufficient PVs. Check StorageClass provisioner: `kubectl get sc`

**Scale-in fails:**
- Cannot scale below the minimum replica count required by the topology (e.g., Raft-based MySQL requires at least 3 replicas).
- Check OpsRequest events: `kubectl describe ops <ops-name> -n <namespace>`

**Data rebalancing after shard scaling:**
- For Redis Cluster, data resharding happens automatically. Monitor with `redis-cli --cluster check`.
- For MongoDB, balancer redistributes chunks. This may take time for large datasets.
