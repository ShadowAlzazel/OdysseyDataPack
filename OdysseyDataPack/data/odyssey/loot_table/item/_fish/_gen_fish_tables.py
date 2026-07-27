#!/usr/bin/env python3
"""
generate_fishing_calls.py

Reads the fish names out of fish_rarity.txt and generates a
"minecraft:fishing" loot table stub for each one, pointing at the
centralized item loot table via minecraft:loot_table, e.g.:

    {
        "type": "minecraft:fishing",
        "pools": [
            {
                "rolls": 1,
                "bonus_rolls": 0,
                "entries": [
                    {
                        "type": "minecraft:loot_table",
                        "value": "odyssey:item/alaska_blackfish"
                    }
                ]
            }
        ],
        "random_sequence": "minecraft:gameplay/fishing"
    }

These are meant to be dropped into wherever your actual fishing loot
tables need to live (you said they're scattered around) -- this script
just generates them in one place so you can grab and move each one.

USAGE
    Run it from inside your fish folder (same one as fish_rarity.txt):
        python generate_fishing_calls.py
    Output goes into a "generated_fishing_calls" subfolder next to this
    script, one <fish>.json per fish. Re-running overwrites that folder's
    contents with the current fish_rarity.txt list.

CONFIG
    NAMESPACE       - namespace prefix for the loot_table value, e.g. "odyssey"
    ITEM_TABLE_PATH - path segment between the namespace and the fish name,
                       e.g. "item" -> "odyssey:item/alaska_blackfish".
                       Set to "item/fish" if your item tables actually live
                       under .../loot_table/item/fish/.
"""

import json
from pathlib import Path

RARITY_FILE = "_fish_rarity.txt"
OUTPUT_DIR_NAME = "generated_fishing_calls"

NAMESPACE = "odyssey"
ITEM_TABLE_PATH = "item"          # -> "odyssey:item/<fish>"
RANDOM_SEQUENCE = "minecraft:gameplay/fishing"


def load_fish_names(folder: Path) -> list:
    path = folder / RARITY_FILE
    if not path.exists():
        print(f"! {RARITY_FILE} not found in {folder}")
        return []

    names = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if ":" in line:
            name = line.split(":", 1)[0].strip()
            if name:
                names.append(name)
    return names


def build_stub(slug: str) -> dict:
    return {
        "type": "minecraft:fishing",
        "pools": [
            {
                "rolls": 1,
                "bonus_rolls": 0,
                "entries": [
                    {
                        "type": "minecraft:loot_table",
                        "value": f"{NAMESPACE}:{ITEM_TABLE_PATH}/{slug}",
                    }
                ],
            }
        ],
        "random_sequence": RANDOM_SEQUENCE,
    }


def main():
    # Always operate on the folder this script lives in, NOT the shell's
    # current working directory.
    folder = Path(__file__).resolve().parent

    fish_names = load_fish_names(folder)
    if not fish_names:
        print("No fish names found -- nothing to generate.")
        return

    out_dir = folder / OUTPUT_DIR_NAME
    out_dir.mkdir(exist_ok=True)

    for slug in fish_names:
        stub = build_stub(slug)
        out_path = out_dir / f"{slug}.json"
        out_path.write_text(json.dumps(stub, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"  ok {out_path.relative_to(folder)}")

    print(f"Done. Generated {len(fish_names)} fishing loot table stub(s) in {out_dir}")


if __name__ == "__main__":
    main()