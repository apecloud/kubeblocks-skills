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
    approved_families = {
        route.removeprefix("kubeblocks-family-")
        for route in reference_only_family_routes()
    }

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

    for item in errors:
        print(f"ERROR: {item}")
    print(f"Checked {len(required)} Tier-1 engine(s), errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
