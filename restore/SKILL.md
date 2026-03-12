---
name: restore
description: Restore KubeBlocks database clusters from backups. Supports full restore (create new cluster from backup) and Point-in-Time Recovery (PITR) to a specific timestamp. Use when the user wants to restore, recover, rebuild, or roll back a database cluster from a backup. Requires an existing backup created by the backup skill. NOT for creating backups (see backup skill) or for creating a brand new cluster without backup data (see create-cluster).
---

# Restore KubeBlocks Database Clusters

## Overview

KubeBlocks supports restoring database clusters from backups. A restore always creates a **new cluster** from an existing backup. Two restore modes are available:

- **Full restore**: Restore from a completed full backup to get the exact state at backup time
- **PITR (Point-in-Time Recovery)**: Restore to any specific timestamp between a full backup and the latest continuous backup

Official docs: https://kubeblocks.io/docs/preview/user_docs/handle-an-exception/recovery

## Workflow

```
- [ ] Step 1: List available backups
- [ ] Step 2: Create a new cluster with restore annotation or OpsRequest
- [ ] Step 3: Verify restored cluster
```

## Step 1: List Available Backups

```bash
kubectl get backup -n <ns>
```

Example output:

```
NAME                  POLICY                              METHOD         STATUS      AGE
mycluster-full        mycluster-mysql-backup-policy        xtrabackup    Completed   2d
mycluster-continuous  mycluster-mysql-backup-policy        archive-binlog Running     2d
```

Check backup details for restore information:

```bash
kubectl describe backup <backup-name> -n <ns>
```

For PITR, note the time range available from the continuous backup's status.

## Step 2: Restore

### Option A: Full Restore via Cluster Annotation

Create a new Cluster CR with the restore annotation. The new cluster spec should match the original cluster's configuration (same component types, resource requests, etc.):

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: <new-cluster>
  namespace: <ns>
  annotations:
    kubeblocks.io/restore-from-backup: '{"<component>":{"name":"<backup-name>","namespace":"<ns>","volumeRestorePolicy":"Parallel"}}'
spec:
  # ... same spec as original cluster ...
```

The `volumeRestorePolicy` options:
- `Parallel` — restore all volumes simultaneously (faster)
- `Serial` — restore volumes one at a time

Apply it:

```bash
kubectl apply -f restored-cluster.yaml
kubectl get cluster <new-cluster> -n <ns> -w
```

### Option B: Full Restore via OpsRequest

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: <new-cluster>-restore-ops
  namespace: <ns>
spec:
  clusterName: <new-cluster>
  type: Restore
  restore:
    backupName: <backup-name>
    backupNamespace: <ns>
```

Apply it:

```bash
kubectl apply -f restore-ops.yaml
kubectl get ops <new-cluster>-restore-ops -n <ns> -w
```

### Option C: PITR Restore (Point-in-Time Recovery)

PITR requires **both** a completed full backup **and** a running continuous backup (archive-binlog for MySQL, wal-archive for PostgreSQL).

Use the annotation method with an additional `restoreTime` field:

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: <new-cluster>
  namespace: <ns>
  annotations:
    kubeblocks.io/restore-from-backup: '{"<component>":{"name":"<continuous-backup>","namespace":"<ns>","volumeRestorePolicy":"Parallel","restoreTime":"2025-01-01T12:00:00Z"}}'
spec:
  # ... same spec as original cluster ...
```

Key points for PITR:
- `name` should reference the **continuous backup** (not the full backup)
- `restoreTime` must be in RFC 3339 format (UTC): `YYYY-MM-DDTHH:MM:SSZ`
- The restore time must fall within the range covered by the full + continuous backups

### Finding the Valid PITR Time Range

```bash
kubectl describe backup <continuous-backup-name> -n <ns>
```

Look for `status.timeRange` which shows the recoverable time window.

## Step 3: Verify Restored Cluster

```bash
# Watch cluster status
kubectl get cluster <new-cluster> -n <ns> -w

# Check pods are running
kubectl get pods -n <ns> -l app.kubernetes.io/instance=<new-cluster>
```

The cluster status should transition to `Running`. Verify data integrity by connecting to the database:

```bash
# Get connection credentials
kubectl get secrets -n <ns> <new-cluster>-<component>-account-root -o jsonpath='{.data.password}' | base64 -d
```

## Troubleshooting

**Restore stuck in Creating:**
- Check backup status is `Completed` (for full) or `Running` (for continuous)
- Verify BackupRepo is accessible: `kubectl get backuprepo`
- Check restore job logs: `kubectl get pods -n <ns> -l app.kubernetes.io/name=restore`

**PITR restore fails:**
- Ensure both full and continuous backups exist
- Verify the `restoreTime` is within the valid time range
- Confirm the continuous backup is still running

**New cluster spec mismatch:**
- The restored cluster spec should match the original (same component definitions, storage size)
- Storage size in the new cluster must be >= the original backup's data size
