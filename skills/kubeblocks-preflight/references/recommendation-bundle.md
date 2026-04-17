# Recommendation Bundle Schema

Use this file as the stable contract between `kubeblocks-preflight` and downstream engine-entry / observability skills.

## Required Shape

```yaml
environmentProfile:
  clusterType: <ack|eks|gke|on-prem|kind|unknown>
  multiAZ: <true|false>
  targetNamespace: <string>
  defaultStorageClassPresent: <true|false>

recommendations:
  storage:
    storageClassName: <string>
    volumeBindingMode: <Immediate|WaitForFirstConsumer|unknown>
    topologyAwareRequired: <true|false>
    allowVolumeExpansion: <true|false|unknown>

  engineEntry:
    recommendedSkill: <skill-name>
    forbiddenGenericPaths:
      - <skill-name>

  sizing:
    defaultTier: <demo|production>

  observability:
    recommendedSkill: <kubeblocks-observability-existing-stack|kubeblocks-observability-bootstrap-stack>
    readinessTarget: <metrics-ready|scrape-ready|dashboard-ready|alerting-ready>

risks:
  - <plain-language risk>
```

## Rules

- `recommendedSkill` must name a real skill path / skill id in this repository.
- `forbiddenGenericPaths` must include `kubeblocks-create-cluster` for high-frequency engines when direct engine-entry skills exist.
- `volumeBindingMode` risk must be explicit for multi-AZ environments.
- `readinessTarget` must not overstate delivery. `metrics-ready` is not the same as `dashboard-ready`.

## Why This Exists

The repository is being refactored so that:

- `preflight` becomes an upstream decision skill
- engine-entry skills no longer need to rediscover storage / monitoring defaults
- regression tests can assert route decisions using a stable contract
