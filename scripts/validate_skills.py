#!/usr/bin/env python3
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from repo_checks import (
    ROOT,
    check_markdown_links,
    extract_frontmatter,
    has_version,
    load_shim_pairs,
    load_yaml,
    load_yaml_rel,
    markdown_files,
    reference_only_family_routes,
    skill_files,
    skill_name_map,
    valid_route_target,
)


def main():
    errors: list[str] = []
    warnings: list[str] = []
    skill_names = set(skill_name_map())
    family_routes = reference_only_family_routes()

    for path in skill_files():
        text = path.read_text(encoding="utf-8")
        frontmatter = extract_frontmatter(text)
        if frontmatter is None:
            errors.append(f"{path.relative_to(ROOT)}: missing frontmatter")
            continue
        if not re.search(r"^name:\s*", frontmatter, re.M):
            errors.append(f"{path.relative_to(ROOT)}: missing name in frontmatter")
        if not has_version(frontmatter):
            errors.append(f"{path.relative_to(ROOT)}: missing version in frontmatter")
        if not re.search(r"^description:\s*", frontmatter, re.M):
            warnings.append(f"{path.relative_to(ROOT)}: missing description in frontmatter")

    for path in sorted(set(markdown_files() + skill_files())):
        check_markdown_links(path, path.read_text(encoding="utf-8"), errors)

    routing_dir = ROOT / "tests/fixtures/routing/tier1"
    routing_fixtures = sorted(routing_dir.glob("*.yaml"))
    if not routing_fixtures:
        errors.append("tests/fixtures/routing/tier1: missing Tier-1 routing fixtures")
    for path in routing_fixtures:
        fixture = load_yaml(path) or {}
        for key in ["engine", "tier", "entry_skill", "required_profiles", "allowed_routes", "forbidden_routes", "required_followups"]:
            if key not in fixture:
                errors.append(f"{path.relative_to(ROOT)}: missing key `{key}`")
        entry_skill = fixture.get("entry_skill")
        if entry_skill and entry_skill not in skill_names:
            errors.append(f"{path.relative_to(ROOT)}: unknown entry_skill `{entry_skill}`")
        for target in fixture.get("required_profiles", []) + fixture.get("allowed_routes", []):
            if not valid_route_target(target, skill_names, family_routes):
                errors.append(f"{path.relative_to(ROOT)}: unknown route target `{target}`")
        if not fixture.get("forbidden_routes"):
            errors.append(f"{path.relative_to(ROOT)}: forbidden_routes must not be empty")
        for target in fixture.get("forbidden_routes", []):
            if not valid_route_target(target, skill_names, family_routes):
                errors.append(f"{path.relative_to(ROOT)}: unknown forbidden target `{target}`")
        followups = fixture.get("required_followups", {})
        for targets in followups.values():
            for target in targets:
                if not valid_route_target(target, skill_names, family_routes):
                    errors.append(f"{path.relative_to(ROOT)}: unknown follow-up target `{target}`")

    coverage_fixture = load_yaml_rel("tests/fixtures/coverage/tier1-required-engines.yaml") or {}
    if not coverage_fixture.get("required_tier1_engines"):
        errors.append("tests/fixtures/coverage/tier1-required-engines.yaml: missing required_tier1_engines")
    min_ops = load_yaml_rel("tests/fixtures/coverage/tier1-min-ops.yaml") or {}
    for key in ["required_columns", "required_status_columns", "allowed_status_values"]:
        if not min_ops.get(key):
            errors.append(f"tests/fixtures/coverage/tier1-min-ops.yaml: missing `{key}`")

    route_matrix = load_yaml_rel("references/routing/route-matrix.yaml") or {}
    for record in route_matrix.get("routes", []):
        for target in record.get("required_profiles", []) + record.get("follow_up_routes", []) + record.get("forbidden_routes", []):
            if not valid_route_target(target, skill_names, family_routes):
                errors.append(f"references/routing/route-matrix.yaml:{record.get('intent')}: unknown target `{target}`")

    shim_pairs = load_shim_pairs()
    shim_fixture_pairs = load_shim_pairs("tests/fixtures/migrations/v1-shims.yaml")
    if shim_pairs != shim_fixture_pairs:
        errors.append("tests/fixtures/migrations/v1-shims.yaml: must stay aligned with references/routing/shim-map.yaml")

    for rel in [
        "references/testing/scenario-matrix.md",
        "references/testing/smoke-checklist.md",
        "references/testing/path-migrations.md",
        "references/routing/shim-map.yaml",
        "references/coverage/engine-tier-map.yaml",
        "references/coverage/addon-capability-matrix.yaml",
        "references/coverage/ops-capability-matrix.yaml",
        "references/routing/route-matrix.yaml",
    ]:
        if not (ROOT / rel).exists():
            errors.append(f"{rel}: missing")

    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"WARNING: {item}")

    print(
        f"Validated {len(skill_files())} SKILL.md file(s), errors={len(errors)}, warnings={len(warnings)}"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
