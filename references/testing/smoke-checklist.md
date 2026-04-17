# Smoke Checklist

Before opening a PR for routing changes:

- Root `SKILL.md` only routes; it does not restate every workflow.
- First-time provisioning paths route through `kubeblocks-preflight`.
- High-frequency engines do not route through `kubeblocks-create-cluster`.
- Observability clearly splits existing-stack vs bootstrap-stack.
- `README.md` uses the same routing language as root `SKILL.md`.
- `tests/fixtures/routes.json` covers both expected routes and prohibited routes.
- `python3 scripts/validate_skills.py` returns zero errors.
