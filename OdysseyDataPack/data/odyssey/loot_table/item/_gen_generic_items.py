import os 
import json
import math

abspath = os.path.abspath(__file__)
dir_name = os.path.dirname(abspath)
os.chdir(dir_name)

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

LOOT_ITEMS = [
    "arcane_book",
    "anodized_titanium_ingot",
    "coagulated_blood",
    "ectoplasm",
    "heated_titanium_ingot",
    "iridium_ingot",
    "blank_tome",
    "alexandrite",
    "jade",
    "jovianite",
    "kunzite",
    "mithril_ingot",
    "neptunian",
    "ruby",
    "silver_ingot",
    "silver_nugget",
    "soul_steel_ingot",
    "titanium_ingot",
    "shadow_trial_key",
    "arcane_armor_trim_smithing_template",
    "danger_armor_trim_smithing_template",
    "imperial_armor_trim_smithing_template",
    "mithril_upgrade_template",
    "soul_steel_upgrade_template",
    "titanium_upgrade_template",
    "iridium_upgrade_template",
    "tome_of_discharge",
    "tome_of_expenditure",
    "tome_of_extraction",
    "tome_of_imitation",
    "tome_of_promotion",
    "tome_of_replication",
    "blade_part_upgrade_template",
    "handle_part_upgrade_template",
    "pommel_part_upgrade_template",
    "hilt_part_upgrade_template",
    "empty_part_upgrade_template",
    "voyager_part_pattern",
    "danger_part_pattern",
    "seraph_part_pattern",
    "marauder_part_pattern",
    "crusader_part_pattern",
    "vandal_part_pattern",
    "imperial_part_pattern",
    "fancy_part_pattern",
    "humble_part_pattern",
    "empty_part_pattern"
]

ITEM_OVERRIDES = {
    "arcane_book": "book",
    "anodized_titanium_ingot": "iron_ingot",
    "coagulated_blood": "rotten_flesh",
    "ectoplasm": "rotten_flesh",
    "heated_titanium_ingot": "iron_ingot",
    "iridium_ingot": "iron_ingot",
    "blank_tome": "book",
    "alexandrite": "emerald",
    "jade": "emerald",
    "jovianite": "emerald",
    "kunzite": "emerald",
    "mithril_ingot": "iron_ingot",
    "neptunian": "emerald",
    "ruby": "emerald",
    "silver_ingot": "iron_ingot",
    "silver_nugget": "iron_nugget",
    "soul_steel_ingot": "iron_ingot",
    "titanium_ingot": "iron_ingot",
    "shadow_trial_key": "trial_key",
    "arcane_armor_trim_smithing_template": "paper",
    "danger_armor_trim_smithing_template": "paper",
    "imperial_armor_trim_smithing_template": "paper",
    "mithril_upgrade_template": "paper",
    "soul_steel_upgrade_template": "paper",
    "titanium_upgrade_template": "paper",
    "iridium_upgrade_template": "paper",
    "tome_of_discharge": "paper",
    "tome_of_expenditure": "paper",
    "tome_of_extraction": "paper",
    "tome_of_imitation": "paper",
    "tome_of_promotion": "paper",
    "tome_of_replication": "paper",
    "blade_part_upgrade_template": "paper",
    "handle_part_upgrade_template": "paper",
    "pommel_part_upgrade_template": "paper",
    "hilt_part_upgrade_template": "paper",
    "empty_part_upgrade_template": "paper",
    "voyager_part_pattern": "paper",
    "danger_part_pattern": "paper",
    "seraph_part_pattern": "paper",
    "marauder_part_pattern": "paper",
    "crusader_part_pattern": "paper",
    "vandal_part_pattern": "paper",
    "imperial_part_pattern": "paper",
    "fancy_part_pattern": "paper",
    "humble_part_pattern": "paper",
    "empty_part_pattern": "paper"
}

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------


# Creation Function
def create_item_file(item_name: str):
    # Create item file name
    filename = f'{item_name}.json'
    # Vars from maps
    global ITEM_OVERRIDES
    override_name = ITEM_OVERRIDES[item_name]
    override_item = f'minecraft:{override_name}'
    
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
    # Combine
    base_json["pools"][0]["entries"][0]["functions"] = [
        set_components, 
        set_name
    ]
    # Write
    text = json.dumps(base_json, indent=2)
    with open(filename, 'w') as file:
        file.write(text)   

# Function to loop through all combinations
def populate_files():
    for item in LOOT_ITEMS:
        create_item_file(item)
    
    
# Main
def main():
    # Prompt 
    print("Confirm Creation of New files? This will overwrite old files.")
    print(f"This will Create {len(LOOT_ITEMS)} items.")
    print("Proceed (y/n) . . .")
    answer = input()
    # Input
    if answer == "y":
        print("Ok")
        populate_files() 
        
# Main
if __name__ == "__main__":
    main()