# Smoke Checklist

Before opening a PR for routing changes:

- Root `SKILL.md` only routes; it does not restate every workflow.
- First-time provisioning paths route through `kubeblocks-preflight`.
- High-frequency engines do not route through `kubeblocks-create-cluster`.
- Observability clearly splits existing-stack vs bootstrap-stack.
- `README.md` uses the same routing language as root `SKILL.md`.
- `references/routing/shim-map.yaml`, `references/routing/route-matrix.yaml`, and `references/testing/path-migrations.md` agree on legacy-name handling.
- Tier-1 routing fixtures forbid both generic fallback and family-as-entry regressions.
- `python3 scripts/validate_skills.py` returns zero errors.
- `python3 scripts/check_addon_coverage.py`, `python3 scripts/check_ops_coverage.py`, and `python3 scripts/check_route_drift.py` return zero errors.
