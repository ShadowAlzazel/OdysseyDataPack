#!/usr/bin/env python3
"""
convert_fish.py

Converts old-style "minecraft:fishing" loot tables (one fish per file) into
the new standardized "chest" item loot table format.

USAGE
    Run it from inside the folder containing your fish loot tables:
        python convert_fish.py
    It only looks at *.json files directly in that folder (no subfolders,
    no path argument needed) and writes backups/fish_rarity.txt there too.

WHAT IT DOES
  - Finds every *.json file directly inside the folder the script is run from
    (does not recurse into subfolders).
  - Skips files that are already converted (top-level "type": "chest").
  - Skips files that aren't "minecraft:fishing" tables (leaves them untouched).
  - For everything else, rewrites the file into the new format:
        * "type": "minecraft:fishing" -> "chest"
        * drops "random_sequence"
        * item_name becomes a plain slug string (e.g. "anchovy")
        * item_model becomes "<NAMESPACE>:<slug>" (e.g. "odyssey:anchovy")
        * adds a minecraft:set_name function using a title-cased display
          name derived from the slug (e.g. "Alaska Blackfish")
        * adds "conditions": [] to set_components
        * adds "weight": 1 to each entry (if not already present)
        * drops minecraft:lore (see fish_rarity.txt below)
  - Before overwriting a file, saves the original into
    "_originals_backup/" (mirroring the folder structure), so nothing
    is lost if something looks wrong.
  - Counts the number of star (star emoji) characters in each fish's old lore
    and records it in fish_rarity.txt as "slug: N". Re-running the script
    merges into that file rather than overwriting it.

CONFIG
    Change NAMESPACE below if your datapack's item_model namespace isn't
    "odyssey".
"""

import json
import re
import shutil
from pathlib import Path

NAMESPACE = "odyssey"           # prefix used for item_model, e.g. "odyssey:anchovy"
RARITY_FILE = "fish_rarity.txt"
BACKUP_DIR_NAME = "_originals_backup"
STAR_CHAR = "\u2b50"             # the star emoji used in old lore


def slugify_from_entry(entry: dict) -> str:
    """Work out a plain slug (e.g. 'anchovy') for this fish entry."""
    for func in entry.get("functions", []):
        if func.get("function") != "minecraft:set_components":
            continue
        components = func.get("components", {})

        model = components.get("minecraft:item_model")
        if isinstance(model, str):
            return model.split(":")[-1]

        name = components.get("minecraft:item_name")
        if isinstance(name, dict) and "translate" in name:
            return name["translate"].split(".")[-1]
        if isinstance(name, str):
            return name.split(":")[-1]

    return entry.get("name", "unknown_fish").split(":")[-1]


def display_name_from_slug(slug: str) -> str:
    """'alaska_blackfish' -> 'Alaska Blackfish'"""
    words = re.split(r"[_\-]+", slug)
    return " ".join(w.capitalize() for w in words if w)


def count_stars(entry: dict) -> int:
    """Count star characters in the old minecraft:lore component, if any."""
    stars = 0
    for func in entry.get("functions", []):
        if func.get("function") != "minecraft:set_components":
            continue
        lore = func.get("components", {}).get("minecraft:lore", [])
        for line in lore:
            text = line.get("text", "") if isinstance(line, dict) else str(line)
            stars += text.count(STAR_CHAR)
    return stars


def convert_entry(entry: dict):
    """Turn one old fishing entry into the new chest-style entry."""
    slug = slugify_from_entry(entry)
    display_name = display_name_from_slug(slug)

    # Preserve any other components that weren't item_name/item_model/lore
    old_components = {}
    for func in entry.get("functions", []):
        if func.get("function") == "minecraft:set_components":
            old_components = dict(func.get("components", {}))
    old_components.pop("minecraft:item_name", None)
    old_components.pop("minecraft:item_model", None)
    old_components.pop("minecraft:lore", None)  # dropped for now, logged separately

    new_components = {
        "minecraft:item_name": slug,
        "minecraft:item_model": f"{NAMESPACE}:{slug}",
    }
    new_components.update(old_components)

    new_entry = {
        "type": "minecraft:item",
        "name": entry.get("name", "minecraft:cod"),
        "functions": [
            {
                "function": "minecraft:set_components",
                "components": new_components,
                "conditions": [],
            },
            {
                "function": "minecraft:set_name",
                "entity": "this",
                "name": {
                    "text": display_name,
                    "bold": False,
                    "italic": False,
                },
            },
        ],
        "weight": entry.get("weight", 1),
    }
    return new_entry, slug, count_stars(entry)


def convert_file(path: Path, rarity_data: dict) -> bool:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"  ! skipped {path} (invalid JSON: {e})")
        return False

    if data.get("type") == "chest":
        print(f"  - skipped {path} (already converted)")
        return False

    if data.get("type") != "minecraft:fishing":
        print(f"  - skipped {path} (type is '{data.get('type')}', not minecraft:fishing)")
        return False

    new_pools = []
    for pool in data.get("pools", []):
        new_entries = []
        for entry in pool.get("entries", []):
            new_entry, slug, stars = convert_entry(entry)
            new_entries.append(new_entry)
            rarity_data[slug] = stars

        new_pools.append({
            "bonus_rolls": float(pool.get("bonus_rolls", 0)),
            "entries": new_entries,
            "rolls": float(pool.get("rolls", 1)),
        })

    new_data = {
        "type": "chest",
        "pools": new_pools,
    }

    # Back up the original before touching it
    backup_path = Path(BACKUP_DIR_NAME) / path.name
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, backup_path)

    path.write_text(json.dumps(new_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  ok converted {path}")
    return True


def main():
    # Always operate on the folder this script lives in, NOT the shell's
    # current working directory — this matters if you invoke the script
    # with a full/relative path from somewhere else (e.g. PowerShell).
    folder = Path(__file__).resolve().parent

    json_files = sorted(folder.glob("*.json"))
    if not json_files:
        print(f"No .json files found in {folder.resolve()}")
        return

    print(f"Scanning {len(json_files)} json file(s) in {folder.resolve()}...")

    rarity_data = {}
    rarity_path = folder / RARITY_FILE
    if rarity_path.exists():
        for line in rarity_path.read_text(encoding="utf-8").splitlines():
            if ":" in line:
                name, val = line.split(":", 1)
                try:
                    rarity_data[name.strip()] = int(val.strip())
                except ValueError:
                    pass

    converted = 0
    for f in json_files:
        if f.name == RARITY_FILE:
            continue
        if convert_file(f, rarity_data):
            converted += 1

    if rarity_data:
        with rarity_path.open("w", encoding="utf-8") as out:
            for slug in sorted(rarity_data):
                out.write(f"{slug}: {rarity_data[slug]}\n")
        print(f"Wrote rarity data for {len(rarity_data)} fish to {rarity_path}")

    print(f"Done. Converted {converted} file(s).")


if __name__ == "__main__":
    main()