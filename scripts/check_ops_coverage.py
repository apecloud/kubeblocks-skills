#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from repo_checks import ROOT, load_yaml_rel


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--addons-repo",
        default=str(ROOT.parent / "kubeblocks-addons"),
        help="Path to the kubeblocks-addons checkout",
    )
    args = parser.parse_args()

    errors: list[str] = []
    addons_repo = Path(args.addons_repo)
    if not addons_repo.exists():
        errors.append(f"addons repo not found: {addons_repo}")

    required = set(
        (load_yaml_rel("tests/fixtures/coverage/tier1-required-engines.yaml") or {}).get(
            "required_tier1_engines", []
        )
    )
    minimums = load_yaml_rel("tests/fixtures/coverage/tier1-min-ops.yaml") or {}
    required_columns = minimums.get("required_columns", [])
    required_status_columns = minimums.get("required_status_columns", [])
    allowed_status_values = set(minimums.get("allowed_status_values", []))

    ops_records = {
        record["engine"]: record
        for record in (load_yaml_rel("references/coverage/ops-capability-matrix.yaml") or {}).get(
            "records", []
        )
    }

    for engine in sorted(required):
        record = ops_records.get(engine)
        if record is None:
            errors.append(f"ops-capability-matrix: missing Tier-1 engine `{engine}`")
            continue

        for column in required_columns + required_status_columns:
            if column not in record:
                errors.append(f"ops-capability-matrix:{engine}: missing `{column}`")
                continue
            value = record.get(column)
            if value not in allowed_status_values:
                errors.append(
                    f"ops-capability-matrix:{engine}: `{column}` must be one of {sorted(allowed_status_values)}"
                )

        evidence_refs = record.get("evidence_refs", [])
        if not evidence_refs:
            errors.append(f"ops-capability-matrix:{engine}: evidence_refs must not be empty")
        for ref in evidence_refs:
            if addons_repo.exists() and not (addons_repo / ref).exists():
                errors.append(f"ops-capability-matrix:{engine}: missing evidence ref {ref}")

    for item in errors:
        print(f"ERROR: {item}")
    print(f"Checked {len(required)} Tier-1 engine(s), errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
