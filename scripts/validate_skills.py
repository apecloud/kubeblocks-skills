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
    require_keys,
    skill_files,
    skill_name_map,
    valid_route_target,
)

ALLOWED_SUPPORT_LEVELS = {"official", "provisional", "examples-only"}
ALLOWED_EVIDENCE_CONFIDENCE = {"high", "medium", "low"}
ALLOWED_READINESS_CEILINGS = {
    "none",
    "metrics-ready",
    "scrape-ready",
    "dashboard-ready",
    "alerting-ready",
}


def require_string_list(
    record: dict,
    key: str,
    label: str,
    errors: list[str],
    *,
    allow_empty: bool = False,
):
    values = record.get(key)
    if not isinstance(values, list):
        errors.append(f"{label}: `{key}` must be a list")
        return
    if not allow_empty and not values:
        errors.append(f"{label}: `{key}` must not be empty")
        return
    for value in values:
        if not isinstance(value, str) or not value:
            errors.append(f"{label}: `{key}` entries must be non-empty strings")


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
    for key in [
        "required_columns",
        "required_status_columns",
        "allowed_status_values",
        "required_enum_columns",
        "allowed_failover_models",
        "allowed_support_levels",
        "allowed_evidence_confidence",
    ]:
        if not min_ops.get(key):
            errors.append(f"tests/fixtures/coverage/tier1-min-ops.yaml: missing `{key}`")

    route_matrix = load_yaml_rel("references/routing/route-matrix.yaml") or {}
    for record in route_matrix.get("routes", []):
        for target in record.get("required_profiles", []) + record.get("follow_up_routes", []) + record.get("forbidden_routes", []):
            if not valid_route_target(target, skill_names, family_routes):
                errors.append(f"references/routing/route-matrix.yaml:{record.get('intent')}: unknown target `{target}`")

    tier1_required = set(coverage_fixture.get("required_tier1_engines", []))
    engine_create_matrix = load_yaml_rel("references/coverage/engine-create-matrix.yaml") or {}
    engine_create_records = {
        record.get("engine"): record for record in engine_create_matrix.get("records", [])
    }
    for engine in sorted(tier1_required):
        label = f"references/coverage/engine-create-matrix.yaml:{engine}"
        record = engine_create_records.get(engine)
        if record is None:
            errors.append(f"{label}: missing Tier-1 record")
            continue
        require_keys(
            record,
            [
                "engine",
                "entry_skill",
                "topology_options",
                "default_topology",
                "service_version_strategy",
                "preflight_requirements",
                "sizing_profiles",
                "connection_methods",
                "next_hops",
                "forbidden_routes",
                "docs_refs",
                "example_refs",
                "core_refs",
                "support_level",
                "evidence_confidence",
            ],
            label,
            errors,
        )
        expected_entry = f"kubeblocks-engine-{engine}"
        if record.get("entry_skill") != expected_entry:
            errors.append(f"{label}: expected entry_skill `{expected_entry}`")
        elif record["entry_skill"] not in skill_names:
            errors.append(f"{label}: unknown entry_skill `{record['entry_skill']}`")
        if record.get("support_level") not in ALLOWED_SUPPORT_LEVELS:
            errors.append(f"{label}: invalid support_level `{record.get('support_level')}`")
        if record.get("evidence_confidence") not in ALLOWED_EVIDENCE_CONFIDENCE:
            errors.append(
                f"{label}: invalid evidence_confidence `{record.get('evidence_confidence')}`"
            )
        require_string_list(record, "docs_refs", label, errors)
        require_string_list(record, "example_refs", label, errors)
        require_string_list(record, "core_refs", label, errors)
        if record.get("default_topology") not in record.get("topology_options", []):
            errors.append(f"{label}: default_topology must be present in topology_options")
        for key in ["preflight_requirements", "sizing_profiles", "connection_methods"]:
            require_string_list(record, key, label, errors)
        for key in ["next_hops", "forbidden_routes"]:
            require_string_list(record, key, label, errors)
            for target in record.get(key, []):
                if not valid_route_target(target, skill_names, family_routes):
                    errors.append(f"{label}: unknown route target `{target}` in `{key}`")

    observability_matrix = load_yaml_rel(
        "references/coverage/observability-capability-matrix.yaml"
    ) or {}
    observability_records = {
        record.get("engine"): record
        for record in observability_matrix.get("records", [])
    }
    for engine in sorted(tier1_required):
        label = f"references/coverage/observability-capability-matrix.yaml:{engine}"
        record = observability_records.get(engine)
        if record is None:
            errors.append(f"{label}: missing Tier-1 record")
            continue
        require_keys(
            record,
            [
                "engine",
                "entry_skill",
                "exporter",
                "scrape_examples",
                "dashboard_examples",
                "alerting_examples",
                "readiness_ceiling",
                "recommended_path",
                "docs_refs",
                "example_refs",
                "core_refs",
                "support_level",
                "evidence_confidence",
            ],
            label,
            errors,
        )
        if record.get("entry_skill") != "kubeblocks-observability-router":
            errors.append(f"{label}: entry_skill must be `kubeblocks-observability-router`")
        elif record["entry_skill"] not in skill_names:
            errors.append(f"{label}: unknown entry_skill `{record['entry_skill']}`")
        if record.get("recommended_path") not in skill_names:
            errors.append(
                f"{label}: unknown recommended_path `{record.get('recommended_path')}`"
            )
        if record.get("readiness_ceiling") not in ALLOWED_READINESS_CEILINGS:
            errors.append(
                f"{label}: invalid readiness_ceiling `{record.get('readiness_ceiling')}`"
            )
        if record.get("support_level") not in ALLOWED_SUPPORT_LEVELS:
            errors.append(f"{label}: invalid support_level `{record.get('support_level')}`")
        if record.get("evidence_confidence") not in ALLOWED_EVIDENCE_CONFIDENCE:
            errors.append(
                f"{label}: invalid evidence_confidence `{record.get('evidence_confidence')}`"
            )
        require_string_list(record, "docs_refs", label, errors)
        require_string_list(
            record,
            "example_refs",
            label,
            errors,
            allow_empty=not bool(record.get("exporter")),
        )
        require_string_list(record, "core_refs", label, errors)

    runtime_contract = load_yaml_rel("references/runtime/runtime-contract.yaml") or {}
    artifacts = runtime_contract.get("artifacts", [])
    if not artifacts:
        errors.append("references/runtime/runtime-contract.yaml: missing `artifacts`")
    for artifact in artifacts:
        label = f"references/runtime/runtime-contract.yaml:{artifact.get('name')}"
        if "template_ref" not in artifact:
            errors.append(f"{label}: missing `template_ref`")
            continue
        template_path = ROOT / artifact["template_ref"]
        if not template_path.exists():
            errors.append(f"{label}: missing template `{artifact['template_ref']}`")
            continue
        if template_path.suffix == ".md":
            text = template_path.read_text(encoding="utf-8")
            for section in artifact.get("required_sections", []):
                if f"## {section}" not in text:
                    errors.append(
                        f"{label}: template `{artifact['template_ref']}` missing heading `{section}`"
                    )
        else:
            template = load_yaml(template_path) or {}
            required_fields = artifact.get("required_fields", [])
            if template_path.name.endswith(".schema.yaml"):
                template_fields = template.get("required_fields", [])
                missing = [field for field in required_fields if field not in template_fields]
                if missing:
                    errors.append(
                        f"{label}: template `{artifact['template_ref']}` missing required_fields {missing}"
                    )
            else:
                for field in required_fields:
                    if field not in template:
                        errors.append(
                            f"{label}: template `{artifact['template_ref']}` missing field `{field}`"
                        )

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
        "references/coverage/engine-create-matrix.yaml",
        "references/coverage/observability-capability-matrix.yaml",
        "references/routing/route-matrix.yaml",
        "references/runtime/runtime-contract.yaml",
        "references/coverage/addon-capability-matrix.schema.yaml",
        "references/coverage/ops-capability-matrix.schema.yaml",
        "references/coverage/engine-create-matrix.schema.yaml",
        "references/coverage/observability-capability-matrix.schema.yaml",
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
