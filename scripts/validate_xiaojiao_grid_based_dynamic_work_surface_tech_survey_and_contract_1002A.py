from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path


STAGE = "1002A_XIAOJIAO_GRID_BASED_DYNAMIC_WORK_SURFACE_TECH_SURVEY_AND_CONTRACT"
FINAL = "XIAOJIAO_GRID_BASED_DYNAMIC_WORK_SURFACE_TECH_SURVEY_AND_CONTRACT_PASS"
SLUG = "xiaojiao_grid_based_dynamic_work_surface_tech_survey_and_contract_1002A"
MARKER = "ALL_1002A_GRID_BASED_DYNAMIC_WORK_SURFACE_TECH_SURVEY_AND_CONTRACT_CHECKS_OK"
REQ_SCHEMA = {
    "surface_mode",
    "grid_layout_schema",
    "zone_type",
    "card_type",
    "card_registry",
    "business_pack_layout_preset",
    "layout_memory_policy",
    "system_recommended_layout",
    "teacher_override_layout",
    "restore_default_layout",
    "card_allowed_zone_rules",
    "drag_resize_boundary_rules",
}
BAD_PARTS = [
    ".env",
    "token",
    "secret",
    "key",
    "node_modules",
    "__pycache__",
    ".db",
    ".sqlite",
    "dist",
    "build",
    "coverage",
    ".DS_Store",
]


def fail(message: str) -> None:
    raise SystemExit(f"VALIDATION_FAILED: {message}")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root")
    args = parser.parse_args()
    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]

    required = [
        f"docs/foundation/{SLUG}.md",
        f"docs/foundation/{SLUG}.json",
        f"samples/{SLUG}/grid_surface_contract_sample_1002A.json",
        f"docs/audit/{SLUG}_result.json",
        f"docs/audit/{SLUG}_report.md",
        f"docs/audit/{SLUG}_checklist.json",
        f"docs/audit_packages/{SLUG}_manifest.json",
        f"scripts/validate_{SLUG}.py",
    ]
    for rel in required:
        if not (root / rel).exists():
            fail(f"missing required file: {rel}")

    contract = load_json(root / f"docs/foundation/{SLUG}.json")
    sample = load_json(root / f"samples/{SLUG}/grid_surface_contract_sample_1002A.json")
    result = load_json(root / f"docs/audit/{SLUG}_result.json")
    manifest = load_json(root / f"docs/audit_packages/{SLUG}_manifest.json")

    if contract.get("stage_code") != STAGE or sample.get("stage_code") != STAGE or result.get("stage_code") != STAGE:
        fail("stage identity mismatch")
    if result.get("final_status") != FINAL or result.get("pass") is not True or result.get("marker") != MARKER:
        fail("result pass/final_status/marker mismatch")
    if set(contract.get("required_schema_parts", [])) != REQ_SCHEMA:
        fail("required schema parts mismatch")

    tech = contract.get("technology_decision", {})
    if tech.get("primary_candidate") != "React-Grid-Layout":
        fail("primary candidate must be React-Grid-Layout")
    if tech.get("secondary_candidate") != "dnd-kit":
        fail("secondary candidate must be dnd-kit")
    if tech.get("backup_candidate") != "Gridstack.js":
        fail("backup candidate must be Gridstack.js")
    if "React Flow" not in tech.get("not_core_surface", []) or "Craft.js" not in tech.get("not_core_surface", []):
        fail("not-core candidates missing")

    modes = {mode.get("mode") for mode in sample.get("surface_modes", [])}
    for mode in ["light_entry", "focus_surface", "grid_deep_studio", "analysis_board"]:
        if mode not in modes:
            fail(f"missing surface mode: {mode}")

    grid = sample.get("grid_layout_schema", {})
    if grid.get("columns") != 12 or grid.get("free_infinite_canvas") is not False:
        fail("grid layout schema mismatch")
    if len(sample.get("business_pack_layout_presets", [])) < 2:
        fail("business pack presets fewer than 2")

    for mapping in [contract.get("hard_boundaries", {}), sample.get("boundary_flags", {}), result.get("boundary_flags", {})]:
        for key, value in mapping.items():
            if value is not False:
                fail(f"unsafe boundary: {key}")

    zip_path = root / f"docs/audit_packages/{SLUG}.zip"
    if not zip_path.exists():
        fail("missing zip")
    with zipfile.ZipFile(zip_path) as zf:
        zip_entries = zf.namelist()
    for entry in zip_entries:
        normalized = entry.replace("\\", "/")
        if normalized.startswith("/") or ":" in normalized or "\\" in entry:
            fail(f"unsafe zip path: {entry}")
        if any(part.lower() in normalized.lower() for part in BAD_PARTS):
            fail(f"forbidden zip entry: {entry}")

    if manifest.get("manifest_minus_zip") != [] or manifest.get("zip_minus_manifest") != []:
        fail("manifest alignment not empty")
    if sorted(manifest.get("zip_entries", [])) != sorted(zip_entries):
        fail("manifest zip entries mismatch")

    print(MARKER)
    return 0


if __name__ == "__main__":
    sys.exit(main())
