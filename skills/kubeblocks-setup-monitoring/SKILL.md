---
name: kubeblocks-setup-monitoring
version: "0.2.0"
description: Compatibility shim for KubeBlocks observability. Use this when the user broadly asks to "set up monitoring"; this skill decides whether to integrate with an existing stack or bootstrap a new one.
---

# Set Up Monitoring for KubeBlocks Clusters

This skill is now a **thin router / shim** for observability.

It exists so older references to `kubeblocks-setup-monitoring` do not break immediately, but the actual execution path must split into one of two leaf skills:

- [kubeblocks-observability-existing-stack](../kubeblocks-observability-existing-stack/SKILL.md)
- [kubeblocks-observability-bootstrap-stack](../kubeblocks-observability-bootstrap-stack/SKILL.md)

## Route Decision

1. If Prometheus / Grafana already exists and should be reused, route to [existing-stack](../kubeblocks-observability-existing-stack/SKILL.md).
2. If no monitoring base exists, route to [bootstrap-stack](../kubeblocks-observability-bootstrap-stack/SKILL.md).

Always be explicit about achieved readiness:

- `metrics-ready`
- `scrape-ready`
- `dashboard-ready`
- `alerting-ready`

Do not say "monitoring is done" when only metrics export exists.

## Compatibility Note

This shim remains in place to preserve old entry names while the repository migrates to the split observability structure.

For addon-specific exporter notes and older Prometheus Operator examples, see [reference.md](references/reference.md).
