#!/usr/bin/env python3
"""
add_rarity.py

Reads fish_rarity.txt (produced by convert_fish.py) and adds a
"minecraft:rarity" component to each already-converted fish item loot
table sitting in this folder, based on star count:

    1 star  -> common
    2 stars -> uncommon
    3 stars -> rare
    4 stars -> epic

If a fish has no entry in fish_rarity.txt, or its star count doesn't map
to anything above (0, 5+, etc.), it defaults to "common".

USAGE
    Run it from inside your fish folder (same one as convert_fish.py):
        python add_rarity.py
    It only touches *.json files sitting directly in this folder (same
    folder the script itself lives in, regardless of your shell's current
    directory), and saves a copy of each file it changes into
    "_rarity_backup/" before writing.

    Safe to re-run: files that already have the correct rarity are
    skipped, and skipped files are noted rather than silently ignored.
"""

import json
import shutil
from pathlib import Path
from typing import Optional

RARITY_FILE = "_fish_rarity.txt"
BACKUP_DIR_NAME = "_rarity_backup"

STAR_TO_RARITY = {
    1: "common",
    2: "uncommon",
    3: "rare",
    4: "epic",
}
DEFAULT_RARITY = "common"


def load_rarity_data(folder: Path) -> dict:
    rarity_data = {}
    path = folder / RARITY_FILE
    if not path.exists():
        print(f"! {RARITY_FILE} not found in {folder} -- everything will default to '{DEFAULT_RARITY}'.")
        return rarity_data
    for line in path.read_text(encoding="utf-8").splitlines():
        if ":" in line:
            name, val = line.split(":", 1)
            try:
                rarity_data[name.strip()] = int(val.strip())
            except ValueError:
                pass
    return rarity_data


def slug_from_components(components: dict) -> Optional[str]:
    model = components.get("minecraft:item_model")
    if isinstance(model, str):
        return model.split(":")[-1]
    name = components.get("minecraft:item_name")
    if isinstance(name, str):
        return name
    return None


def add_rarity_to_file(path: Path, rarity_data: dict, folder: Path) -> bool:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"  ! skipped {path.name} (invalid JSON: {e})")
        return False

    if data.get("type") != "chest":
        print(f"  - skipped {path.name} (type is '{data.get('type')}', not a converted item table)")
        return False

    changed = False
    touched_any_entry = False
    for pool in data.get("pools", []):
        for entry in pool.get("entries", []):
            for func in entry.get("functions", []):
                if func.get("function") != "minecraft:set_components":
                    continue
                touched_any_entry = True
                components = func.setdefault("components", {})
                slug = slug_from_components(components)

                stars = rarity_data.get(slug) if slug else None
                rarity = STAR_TO_RARITY.get(stars, DEFAULT_RARITY)

                if components.get("minecraft:rarity") != rarity:
                    components["minecraft:rarity"] = f'{rarity}'
                    changed = True

    if not touched_any_entry:
        print(f"  - skipped {path.name} (no set_components function found)")
        return False

    if not changed:
        print(f"  - skipped {path.name} (rarity already up to date)")
        return False

    backup_path = folder / BACKUP_DIR_NAME / path.name
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, backup_path)

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  ok {path.name}")
    return True


def main():
    # Always operate on the folder this script lives in, NOT the shell's
    # current working directory.
    folder = Path(__file__).resolve().parent
    rarity_data = load_rarity_data(folder)

    json_files = sorted(folder.glob("*.json"))
    if not json_files:
        print(f"No .json files found in {folder}")
        return

    print(f"Applying rarity to {len(json_files)} json file(s) in {folder}...")

    updated = 0
    for f in json_files:
        if add_rarity_to_file(f, rarity_data, folder):
            updated += 1

    print(f"Done. Updated {updated} file(s).")


if __name__ == "__main__":
    main()