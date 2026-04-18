#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from repo_checks import ROOT, load_yaml_rel, reference_only_family_routes


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Cross-check Tier-1 addon coverage against the local kubeblocks-addons repo. "
            "This script requires a kubeblocks-addons checkout."
        )
    )
    parser.add_argument(
        "--addons-repo",
        default=str(ROOT.parent / "kubeblocks-addons"),
        help="Path to the kubeblocks-addons checkout (default: ../kubeblocks-addons)",
    )
    args = parser.parse_args()

    errors: list[str] = []
    addons_repo = Path(args.addons_repo)
    if not addons_repo.exists():
        errors.append(
            "addons repo not found: "
            f"{addons_repo} (clone kubeblocks-addons as ../kubeblocks-addons or pass --addons-repo)"
        )

    required = set(
        (load_yaml_rel("tests/fixtures/coverage/tier1-required-engines.yaml") or {}).get(
            "required_tier1_engines", []
        )
    )
    tier_map = {
        record["engine"]: record
        for record in (load_yaml_rel("references/coverage/engine-tier-map.yaml") or {}).get(
            "records", []
        )
    }
    addon_matrix = {
        record["engine"]: record
        for record in (
            load_yaml_rel("references/coverage/addon-capability-matrix.yaml") or {}
        ).get("records", [])
    }
    addon_schema = load_yaml_rel("references/coverage/addon-capability-matrix.schema.yaml") or {}
    approved_families = {
        route.removeprefix("kubeblocks-family-")
        for route in reference_only_family_routes()
    }
    allowed_support_levels = set(addon_schema.get("allowed_support_levels", []))
    allowed_evidence_confidence = set(
        addon_schema.get("allowed_evidence_confidence", [])
    )

    for engine in sorted(required):
        tier_record = tier_map.get(engine)
        if tier_record is None:
            errors.append(f"engine-tier-map: missing Tier-1 engine `{engine}`")
        else:
            if tier_record.get("tier") != "tier1-dedicated":
                errors.append(f"engine-tier-map:{engine}: expected tier1-dedicated")
            if tier_record.get("entry_skill") != f"kubeblocks-engine-{engine}":
                errors.append(
                    f"engine-tier-map:{engine}: expected entry_skill kubeblocks-engine-{engine}"
                )
            if tier_record.get("generic_allowed") is not False:
                errors.append(f"engine-tier-map:{engine}: generic_allowed must be false")
            family = tier_record.get("family")
            if family is not None and family not in approved_families:
                errors.append(f"engine-tier-map:{engine}: unsupported family `{family}`")

        addon_record = addon_matrix.get(engine)
        if addon_record is None:
            errors.append(f"addon-capability-matrix: missing Tier-1 engine `{engine}`")
            continue

        if addon_record.get("tier") != "tier1-dedicated":
            errors.append(f"addon-capability-matrix:{engine}: expected tier1-dedicated")
        if addon_record.get("entry_skill") != f"kubeblocks-engine-{engine}":
            errors.append(
                f"addon-capability-matrix:{engine}: expected entry_skill kubeblocks-engine-{engine}"
            )
        if not addon_record.get("example_refs"):
            errors.append(f"addon-capability-matrix:{engine}: example_refs must not be empty")
        if not addon_record.get("docs_refs"):
            errors.append(f"addon-capability-matrix:{engine}: docs_refs must not be empty")
        if not addon_record.get("core_refs"):
            errors.append(f"addon-capability-matrix:{engine}: core_refs must not be empty")
        if addon_record.get("support_level") not in allowed_support_levels:
            errors.append(
                f"addon-capability-matrix:{engine}: invalid support_level `{addon_record.get('support_level')}`"
            )
        if addon_record.get("evidence_confidence") not in allowed_evidence_confidence:
            errors.append(
                "addon-capability-matrix:"
                f"{engine}: invalid evidence_confidence `{addon_record.get('evidence_confidence')}`"
            )

        addon_repo_path = addon_record.get("addon_repo_path")
        if not addon_repo_path:
            errors.append(f"addon-capability-matrix:{engine}: addon_repo_path missing")
        elif addons_repo.exists() and not (addons_repo / addon_repo_path).exists():
            errors.append(
                f"addon-capability-matrix:{engine}: missing addon_repo_path {addon_repo_path}"
            )

        for ref in addon_record.get("example_refs", []):
            if addons_repo.exists() and not (addons_repo / ref).exists():
                errors.append(f"addon-capability-matrix:{engine}: missing example ref {ref}")
        for ref in addon_record.get("core_refs", []):
            if not str(ref).startswith("kubeblocks-core:"):
                errors.append(
                    f"addon-capability-matrix:{engine}: core_ref must start with `kubeblocks-core:` ({ref})"
                )

    for item in errors:
        print(f"ERROR: {item}")
    print(f"Checked {len(required)} Tier-1 engine(s), errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
