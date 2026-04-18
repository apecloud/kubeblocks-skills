---
name: kubeblocks-observability-router
version: "0.1.0"
description: Primary observability entry for KubeBlocks-managed databases. Use this when the user broadly asks for monitoring or observability and you need to choose between integrating with an existing stack, bootstrapping a new stack, or declaring the current readiness level. The legacy kubeblocks-setup-monitoring skill remains only as a compatibility shim.
---

# Observability Router

- If Prometheus/Grafana already exists, route to [kubeblocks-observability-existing-stack](../kubeblocks-observability-existing-stack/SKILL.md).
- If no monitoring base exists, route to [kubeblocks-observability-bootstrap-stack](../kubeblocks-observability-bootstrap-stack/SKILL.md).
- Always state whether the current state is only `metrics-ready`, `scrape-ready`, `dashboard-ready`, or `alerting-ready`.
