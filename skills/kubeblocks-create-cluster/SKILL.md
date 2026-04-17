---
name: kubeblocks-create-cluster
version: "0.2.0"
description: Create a database cluster on KubeBlocks using a generic Cluster CR template. This skill is only the fallback for engines without a dedicated addon-* entry skill. Do not use it for MySQL, PostgreSQL, Redis, MongoDB, or Kafka.
---

# Create a Database Cluster on KubeBlocks

This skill is the **other-addons fallback**.

Use it only when:

- the target engine does not have a dedicated `addon-*` entry skill
- KubeBlocks is already installed
- preflight has already produced storage and routing recommendations

Do **not** use this skill for:

- MySQL -> [kubeblocks-addon-mysql](../kubeblocks-addon-mysql/SKILL.md)
- PostgreSQL -> [kubeblocks-addon-postgresql](../kubeblocks-addon-postgresql/SKILL.md)
- Redis -> [kubeblocks-addon-redis](../kubeblocks-addon-redis/SKILL.md)
- MongoDB -> [kubeblocks-addon-mongodb](../kubeblocks-addon-mongodb/SKILL.md)
- Kafka -> [kubeblocks-addon-kafka](../kubeblocks-addon-kafka/SKILL.md)

If rollout readiness is still unknown, stop and run [kubeblocks-preflight](../kubeblocks-preflight/SKILL.md) first.

## Workflow

```text
- [ ] Step 1: Confirm this is truly an other-addons case
- [ ] Step 2: Gather clusterDef / topology / component names from the environment
- [ ] Step 3: Fill the generic Cluster template
- [ ] Step 4: Validate and apply
- [ ] Step 5: Verify the cluster becomes Running
```

## Step 1: Confirm This Is Truly An Other-Addons Case

Before using the generic path, answer both questions:

1. Does the engine already have a dedicated `addon-*` skill in this repository?
2. Has preflight already selected storage, sizing, and namespace defaults?

If the answer to either question is "no", stop and route correctly first.

## Step 2: Gather Engine-Specific Values

Use the live cluster to discover the needed values:

```bash
kubectl get clusterdefinitions
kubectl get componentversions
```

Record:

- `clusterDef`
- `topology`
- component name
- `serviceVersion`
- `storageClassName`

## Step 3: Fill The Generic Template

This is a placeholder template for engines that do not have a dedicated entry skill.

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: <cluster-name>
  namespace: <namespace>
spec:
  clusterDef: <clusterDef-from-environment>
  topology: <topology-from-environment>
  terminationPolicy: Delete
  componentSpecs:
    - name: <component-name>
      serviceVersion: "<serviceVersion>"
      replicas: <replica-count>
      resources:
        requests:
          cpu: "<cpu-request>"
          memory: "<memory-request>"
        limits:
          cpu: "<cpu-limit>"
          memory: "<memory-limit>"
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            storageClassName: <storageClassName-from-preflight>
            resources:
              requests:
                storage: <storage-size>
```

This template is intentionally generic. It does not try to encode the topology advice for high-frequency engines.

## Step 4: Validate And Apply

```bash
kubectl apply -f cluster.yaml --dry-run=server
kubectl apply -f cluster.yaml
```

## Step 5: Verify

```bash
kubectl get cluster -n <namespace> <cluster-name> -w
kubectl get pods -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

## Exit Criteria

This path is complete only when:

- the engine truly belongs to `other-addons`
- storage choice comes from preflight, not guesswork
- the cluster reaches `Running`

For connection examples and deep engine-specific operations, rely on the relevant addon skill or official addon docs instead of expanding this fallback into another high-frequency entry path.
