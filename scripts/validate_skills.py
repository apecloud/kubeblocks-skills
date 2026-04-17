#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_FILES = sorted(ROOT.rglob("SKILL.md"))
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def extract_frontmatter(text: str):
    if not text.startswith("---\n"):
        return None
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return None
    return parts[0][4:]


def has_version(frontmatter: str) -> bool:
    if re.search(r"^version:\s*['\"]?[^'\"]+['\"]?\s*$", frontmatter, re.M):
        return True
    if re.search(r"^metadata:\s*$", frontmatter, re.M) and re.search(
        r"^\s+version:\s*['\"]?[^'\"]+['\"]?\s*$", frontmatter, re.M
    ):
        return True
    return False


def check_markdown_links(path: Path, text: str, errors: list[str], warnings: list[str]):
    for match in LINK_PATTERN.finditer(text):
        target = match.group(1)
        if target.startswith("http://") or target.startswith("https://") or target.startswith("#"):
            continue
        if target.startswith("mailto:"):
            continue
        file_part = target.split("#", 1)[0]
        if not file_part:
            continue
        resolved = (path.parent / file_part).resolve()
        if not resolved.exists():
            errors.append(f"{path.relative_to(ROOT)}: broken link -> {target}")


def main():
    errors: list[str] = []
    warnings: list[str] = []

    for path in SKILL_FILES:
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

    for rel in ["README.md", "SKILL.md"]:
        path = ROOT / rel
        check_markdown_links(path, path.read_text(encoding="utf-8"), errors, warnings)

    fixtures_path = ROOT / "tests/fixtures/routes.json"
    if not fixtures_path.exists():
        errors.append("tests/fixtures/routes.json: missing route fixtures file")
    else:
        fixtures = json.loads(fixtures_path.read_text(encoding="utf-8"))
        for fixture in fixtures:
            expected = ROOT / fixture["expected_route"]
            if not expected.exists():
                errors.append(f"routes.json:{fixture['id']}: missing expected_route target {fixture['expected_route']}")
            prohibited = fixture.get("prohibited_routes", [])
            if not prohibited:
                errors.append(f"routes.json:{fixture['id']}: prohibited_routes must not be empty")
            for route in prohibited:
                if not (ROOT / route).exists():
                    errors.append(f"routes.json:{fixture['id']}: missing prohibited route target {route}")

    for rel in [
        "references/testing/scenario-matrix.md",
        "references/testing/smoke-checklist.md",
        "references/testing/path-migrations.md",
    ]:
        if not (ROOT / rel).exists():
            errors.append(f"{rel}: missing")

    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"WARNING: {item}")

    print(
        f"Validated {len(SKILL_FILES)} SKILL.md file(s), errors={len(errors)}, warnings={len(warnings)}"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
