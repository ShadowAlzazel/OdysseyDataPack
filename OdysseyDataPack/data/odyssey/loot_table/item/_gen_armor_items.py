import os 
import json
import math

abspath = os.path.abspath(__file__)
dir_name = os.path.dirname(abspath)
os.chdir(dir_name)

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------


# List
equippables = ['helmet', 'chestplate', 'leggings', 'boots']
materials = ['silver', 'copper', 'soul_steel', 'titanium', 'anodized_titanium', 'iridium', 'mithril']

# Maps
body_slots = {
    'helmet': 'head', 
    'chestplate': 'chest',
    'leggings': 'legs', 
    'boots': 'feet'
}
body_index = {
    'helmet': 0, 
    'chestplate': 1,
    'leggings': 2, 
    'boots': 3
}
ARMOR_VALUES = {
    'copper': [2, 4, 3, 1],
    'silver': [3, 5, 3, 2], 
    'soul_steel': [3, 7, 6, 3],
    'titanium': [3, 7, 6, 3], 
    'anodized_titanium': [3, 7, 6, 3],
    'iridium': [4, 9, 7, 4],
    'mithril': [4, 8, 6, 3]
}
TOUGHNESS_VALUES = {
    'copper': [1, 1, 1, 1],
    'silver': [1, 1, 1, 1], 
    'soul_steel': [2, 2, 2, 2],
    'titanium': [2, 2, 2, 2], 
    'anodized_titanium': [2, 2, 2, 2],
    'iridium': [3, 3, 3, 3],
    'mithril': [4, 4, 4, 4]
}

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------


# Creation Function
def create_armor_file(material, equippable):
    # Create item file name
    filename = f'{material}_{equippable}.json'
    # Vars from maps
    slot = f'{body_slots[equippable]}'
    item_name = f'{material}_{equippable}'
    override_item = f'minecraft:iron_{equippable}'
    
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
        "function": "minecraft:set_components",
        "components": {
            "minecraft:item_name": item_name,
            "minecraft:equippable": {
                "asset_id": f'odyssey:{material}',
                "slot": slot,
                "equip_sound": "item.armor.equip_chain"
            },
            "minecraft:item_model": f'odyssey:{item_name}'
        },
        "conditions": []
    }
    set_name = {
        "function": "minecraft:set_name",
        "entity": "this",
        "name": {
            "text": f'{material} {equippable}'.replace("_", " ").title(),
            "bold": False,
            "italic": False
        }
    }
    value_index = body_index[equippable]
    armor_value = ARMOR_VALUES[material][value_index]
    armor_toughness = TOUGHNESS_VALUES[material][value_index]
    set_attributes = {
        "function": "minecraft:set_attributes",
        "modifiers": [
            {
                "attribute": "minecraft:armor",
                "operation": "add_value",
                "amount": armor_value,
                "id": f'odyssey:item.base_armor.{equippable}',
                "slot": slot
            },
            {
                "attribute": "minecraft:armor_toughness",
                "operation": "add_value",
                "amount": armor_toughness,
                "id": f'odyssey:item.base_armor_toughness.{equippable}',
                "slot": slot
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
    for mat in materials:
        for equip in equippables:
            create_armor_file(mat, equip)
        
# Main
def main():
    # Prompt 
    print("Confirm Creation of New files? This will overwrite old files.")
    print(f"Will Create {len(materials) * len(equippables)} armor items.")
    print("Proceed (y/n) . . .")
    answer = input()
    # Input
    if answer == "y":
        print("Ok")
        populate_files() 
        
# Main
if __name__ == "__main__":
    main()