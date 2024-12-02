import os 
import json
import math
from dataclasses import dataclass

abspath = os.path.abspath(__file__)
dir_name = os.path.dirname(abspath)
os.chdir(dir_name)

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

@dataclass
class GlyphData:
    item_override: str="brick"
    attribute: str
    value: int
    slot_group: float=2.4
    

GLYPH_ITEMS: dict[str, GlyphData] = {

}

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------


# Creation Function
def create_item_file(item_name: str):
    # Create item file name
    global GLYPH_ITEMS
    item_data: GlyphData = GLYPH_ITEMS[item_name]
    filename = f'{item_name}.json'
    override_item = f'minecraft:{item_data.item_override}'
    # Base json
    base_json = {
        "pools": [{
            "bonus_rolls": 0.0,
            "entries": [{
                "type": "minecraft:item",
                "name": override_item,
                "functions": [],
                "weight": 1
            }],
            "rolls": 1.0
        }]
    }
    # function jsons
    set_components = {
        "function": "set_components",
        "components": {
            "minecraft:item_name": item_name,
            "minecraft:item_model": f'odyssey:{item_name}'
        },
        "conditions": []
    }
    set_name = {
        "function": "minecraft:set_name",
        "entity": "this",
        "name": {
            "text": f'{item_name}'.replace("_", " ").title(),
            "bold": False,
            "italic": False
        }
    }
    set_attributes = {
        "function": "minecraft:set_attributes",
        "modifiers": [
            {
                "attribute": attribute,
                "operation": "add_value",
                "amount": value,
                "id": f'odyssey:item.glyph_slot',
                "slot": slot_group
            }
        ]
    }
    # Combine
    base_json["pools"][0]["entries"][0]["functions"] = [
        set_components, 
        set_name,
        set_attributes
    ]
    # Write
    text = json.dumps(base_json, indent=2)
    with open(filename, 'w') as file:
        file.write(text)   


# Function to loop through all combinations
def populate_files():
    for key in GLYPH_ITEMS:
        create_item_file(key)
    
# Main
def main():
    # Prompt 
    print("Confirm Creation of New files? This will overwrite old files.")
    print(f"This will Create {len(GLYPH_ITEMS)} items.")
    print("Proceed (y/n) . . .")
    answer = input()
    # Input
    if answer == "y":
        print("Ok")
        populate_files() 
        
# Main
if __name__ == "__main__":
    main()