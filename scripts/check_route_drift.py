#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from repo_checks import (
    ROOT,
    load_path_migration_skill_pairs,
    load_shim_pairs,
    load_yaml_rel,
    reference_only_family_routes,
    skill_name_map,
    valid_route_target,
)


def main():
    errors: list[str] = []
    skill_names = set(skill_name_map())
    family_routes = reference_only_family_routes()
    shim_pairs = load_shim_pairs()
    migration_pairs = load_shim_pairs("tests/fixtures/migrations/v1-shims.yaml")
    path_migration_map, path_migration_duplicates, path_migration_malformed = (
        load_path_migration_skill_pairs()
    )
    path_migration_pairs = set(path_migration_map.items())

    if shim_pairs != migration_pairs:
        missing = shim_pairs - migration_pairs
        extra = migration_pairs - shim_pairs
        if missing:
            errors.append(f"v1-shims fixture missing shim-map pairs: {sorted(missing)}")
        if extra:
            errors.append(f"v1-shims fixture has extra pairs not in shim-map: {sorted(extra)}")

    if shim_pairs != path_migration_pairs:
        missing = shim_pairs - path_migration_pairs
        extra = path_migration_pairs - shim_pairs
        if missing:
            errors.append(f"path-migrations.md missing shim-map pairs: {sorted(missing)}")
        if extra:
            errors.append(f"path-migrations.md has extra exact shim pairs not in shim-map: {sorted(extra)}")

    for lineno, legacy_skill, previous_target, duplicate_target in path_migration_duplicates:
        errors.append(
            "path-migrations.md:"
            f"{lineno}: duplicate legacy skill `{legacy_skill}` maps to "
            f"`{previous_target}` and `{duplicate_target}`"
        )

    for lineno, legacy_cell, new_cell in path_migration_malformed:
        errors.append(
            "path-migrations.md:"
            f"{lineno}: exact shim rows must use `` `kubeblocks-*` | `kubeblocks-*` `` cells, got "
            f"`{legacy_cell}` -> `{new_cell}`"
        )

    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    agents_text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    root_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if "kubeblocks-family-" in readme_text or "kubeblocks-family-" in root_text:
        errors.append("README.md / SKILL.md must not expose kubeblocks-family-* as executable routes")
    if "not a cold-start create-time primary entry" not in readme_text:
        errors.append("README.md must explicitly state that family is not a cold-start primary entry")
    if "only this repo" not in readme_text:
        errors.append("README.md must explicitly state that runtime should work with only this repo")
    if "not runtime prerequisites" not in readme_text:
        errors.append("README.md must explicitly state that addon/core repos are not runtime prerequisites")
    if "optional secondary evidence" not in readme_text:
        errors.append("README.md must explicitly allow addon/core repos only as optional secondary evidence")
    if "only this repo" not in agents_text:
        errors.append("AGENTS.md must explicitly state that runtime should work with only this repo")
    if "not runtime prerequisites" not in agents_text:
        errors.append("AGENTS.md must explicitly state that addon/core repos are not runtime prerequisites")
    if "optional secondary evidence" not in agents_text:
        errors.append("AGENTS.md must explicitly allow addon/core repos only as optional secondary evidence")
    if "family/taxonomy-only explanation layer" not in root_text:
        errors.append("SKILL.md must explicitly forbid routing Tier-1 engines to family")
    if "Do **not** require `kubeblocks-addons` or KubeBlocks core repo checkouts as runtime prerequisites." not in root_text:
        errors.append("SKILL.md must explicitly forbid runtime dependence on kubeblocks-addons/core checkouts")
    for legacy_skill, _new_skill in sorted(shim_pairs):
        if legacy_skill == "kubeblocks-setup-monitoring":
            continue
        root_link = f"skills/{legacy_skill}/SKILL.md"
        readme_link = f"./skills/{legacy_skill}/SKILL.md"
        if root_link in root_text or readme_link in readme_text:
            errors.append(
                f"README.md / SKILL.md must not present legacy shim `{legacy_skill}` as a main entry"
            )

    route_matrix = load_yaml_rel("references/routing/route-matrix.yaml") or {}
    route_records = {record["intent"]: record for record in route_matrix.get("routes", [])}
    required = (load_yaml_rel("tests/fixtures/coverage/tier1-required-engines.yaml") or {}).get(
        "required_tier1_engines", []
    )

    for engine in required:
        intent = f"create-{engine}"
        record = route_records.get(intent)
        if record is None:
            errors.append(f"route-matrix: missing intent `{intent}`")
            continue
        fixture = load_yaml_rel(f"tests/fixtures/routing/tier1/{engine}.yaml") or {}
        dedicated = f"kubeblocks-engine-{engine}"
        if dedicated not in record.get("follow_up_routes", []):
            errors.append(f"route-matrix:{intent}: missing follow_up route `{dedicated}`")
        if fixture.get("entry_skill") != dedicated:
            errors.append(f"tests/fixtures/routing/tier1/{engine}.yaml: entry_skill must be `{dedicated}`")
        for profile in fixture.get("required_profiles", []):
            if profile not in record.get("required_profiles", []):
                errors.append(f"route-matrix:{intent}: missing required profile `{profile}` from fixture")
        for target in fixture.get("allowed_routes", []):
            if target not in record.get("follow_up_routes", []):
                errors.append(f"route-matrix:{intent}: missing allowed route `{target}` from fixture")
        if "kubeblocks-engine-generic" not in record.get("forbidden_routes", []):
            errors.append(f"route-matrix:{intent}: must forbid kubeblocks-engine-generic")
        if "kubeblocks-create-cluster" not in record.get("forbidden_routes", []):
            errors.append(f"route-matrix:{intent}: must forbid kubeblocks-create-cluster")
        for target in fixture.get("forbidden_routes", []):
            if target not in record.get("forbidden_routes", []):
                errors.append(f"route-matrix:{intent}: missing forbidden route `{target}` from fixture")
        for target in record.get("required_profiles", []) + record.get("follow_up_routes", []) + record.get("forbidden_routes", []):
            if not valid_route_target(target, skill_names, family_routes):
                errors.append(f"route-matrix:{intent}: unknown target `{target}`")

    generic_route = route_records.get("create-other-engine")
    if generic_route is None or "kubeblocks-engine-generic" not in generic_route.get(
        "follow_up_routes", []
    ):
        errors.append("route-matrix:create-other-engine must follow up to kubeblocks-engine-generic")

    for legacy_skill, new_skill in sorted(shim_pairs):
        if legacy_skill not in skill_names:
            errors.append(f"shim-map: missing legacy skill `{legacy_skill}` in repo")
        if new_skill not in skill_names:
            errors.append(f"shim-map: missing new skill `{new_skill}` in repo")

    for item in errors:
        print(f"ERROR: {item}")
    print(f"Checked {len(required)} Tier-1 route(s), errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
