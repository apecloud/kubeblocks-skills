# Frontmatter Schema

## Target Schema

New or heavily rewritten skills should converge on:

```yaml
---
name: <skill-name>
version: "<semver>"
description: <one-line description>
---
```

## Migration Note

The repository still contains older skills that use:

```yaml
metadata:
  version: "0.1.0"
```

The first refactor batch does **not** normalize every file at once. Validation currently accepts either form, but new work should prefer top-level `version`.
