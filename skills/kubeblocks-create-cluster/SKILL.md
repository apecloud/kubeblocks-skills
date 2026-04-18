---
name: kubeblocks-create-cluster
version: "0.2.0"
description: Legacy compatibility shim for the generic KubeBlocks create path. The primary create-time fallback is now kubeblocks-engine-generic. Keep this skill callable for older references, but do not recommend it as the main path for cold-start agents.
---

# Legacy Shim: Generic Create Path

The primary generic create-time entry is now [kubeblocks-engine-generic](../kubeblocks-engine-generic/SKILL.md).

Keep this legacy name available for older prompts and saved paths, but do **not** recommend it as the primary create route.

## Compatibility Rule

If a request lands here:

1. Route back to [kubeblocks-engine-generic](../kubeblocks-engine-generic/SKILL.md) unless the user explicitly needs the preserved legacy wording below.
2. Never keep Tier-1 engines on this path.
3. Keep `kubeblocks-preflight` as the gate before any generic manifest is applied.

## Preserved Legacy Reference

The preserved generic template and notes remain in [reference.md](references/reference.md) for backwards compatibility.
