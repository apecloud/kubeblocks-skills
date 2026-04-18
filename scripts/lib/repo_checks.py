from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
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


def load_yaml(path: Path):
    result = subprocess.run(
        [
            "ruby",
            "-ryaml",
            "-rjson",
            "-e",
            "puts JSON.generate(YAML.load_file(ARGV[0]))",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"failed to parse YAML: {path}")
    return json.loads(result.stdout) if result.stdout.strip() else None


def load_yaml_rel(relative_path: str):
    return load_yaml(ROOT / relative_path)


def skill_files():
    return sorted(ROOT.rglob("SKILL.md"))


def skill_name_map():
    mapping = {}
    for path in skill_files():
        frontmatter = extract_frontmatter(path.read_text(encoding="utf-8"))
        if frontmatter is None:
            continue
        match = re.search(r"^name:\s*['\"]?([^\n'\"]+)['\"]?\s*$", frontmatter, re.M)
        if match:
            mapping[match.group(1)] = path
    return mapping


def reference_only_family_routes():
    data = load_yaml_rel("references/coverage/engine-tier-map.yaml") or {}
    return {
        f"kubeblocks-family-{family}"
        for family in data.get("reference_only_families", [])
    }


def check_markdown_links(path: Path, text: str, errors: list[str]):
    for match in LINK_PATTERN.finditer(text):
        target = match.group(1)
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        file_part = target.split("#", 1)[0]
        if not file_part:
            continue
        resolved = (path.parent / file_part).resolve()
        if not resolved.exists():
            errors.append(f"{path.relative_to(ROOT)}: broken link -> {target}")


def markdown_files():
    files = [ROOT / "README.md", ROOT / "SKILL.md"]
    files.extend(sorted((ROOT / "references/routing").glob("*.md")))
    files.extend(sorted((ROOT / "references/testing").glob("*.md")))
    return files


def valid_route_target(target: str, skill_names: set[str], family_routes: set[str]) -> bool:
    return target in skill_names or target in family_routes


def load_shim_pairs(relative_path: str = "references/routing/shim-map.yaml"):
    data = load_yaml_rel(relative_path) or {}
    return {
        (record["legacy_skill"], record["new_skill"])
        for record in data.get("shims", [])
    }


def load_path_migration_skill_pairs(
    relative_path: str = "references/testing/path-migrations.md",
):
    text = (ROOT / relative_path).read_text(encoding="utf-8")
    pairs: dict[str, str] = {}
    duplicates: list[tuple[int, str, str, str]] = []
    malformed: list[tuple[int, str, str]] = []

    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 2:
            continue
        if set(cells[0]) == {"-"} and set(cells[1]) == {"-"}:
            continue

        old_match = re.fullmatch(r"`(kubeblocks-[a-z0-9-]+)`", cells[0])
        new_match = re.fullmatch(r"`(kubeblocks-[a-z0-9-]+)`", cells[1])
        if old_match is None and new_match is None:
            continue
        if old_match is None or new_match is None:
            malformed.append((lineno, cells[0], cells[1]))
            continue

        legacy_skill = old_match.group(1)
        new_skill = new_match.group(1)
        previous = pairs.get(legacy_skill)
        if previous is not None:
            duplicates.append((lineno, legacy_skill, previous, new_skill))
            continue
        pairs[legacy_skill] = new_skill

    return pairs, duplicates, malformed


def require_keys(record: dict, keys: list[str], label: str, errors: list[str]):
    for key in keys:
        if key not in record:
            errors.append(f"{label}: missing key `{key}`")
