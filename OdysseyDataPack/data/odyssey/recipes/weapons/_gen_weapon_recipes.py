import os 
import json

from _weapon_data import *

abspath = os.path.abspath(__file__)
dir_name = os.path.dirname(abspath)
os.chdir(dir_name)

# TODO 
# Add [Polexe], [Battleaxe(labrys)]
# Rework [Rapier], [Lance]

#tool_types = ['chakram', 'claymore', 'cutlass', 'dagger', 'halberd', 'katana', 'kunai', 'lance', 
#                'longaxe', 'longsword', 'rapier', 'saber', 'scythe', 'sickle', 'spear', 'warhammer']
#materials = ['wooden', 'golden', 'stone', 'iron', 'diamond', 'netherite',
#             'copper', 'silver', 'soul_steel', 'titanium', 'andonized_titanium', 'iridium', 'mithril']

# Function to create weapon recipe files 
def create_weapon_recipe_files(): 
    for i in range(len(materials)):
        for j in range(len(tool_types)):
            mat: Material = materials[i]
            ttyp: ToolType = tool_types[j]
            # Create variables for names
            item_name = f'{mat.name}_{ttyp.name}'
            custom_name = f'{mat.material_name} {ttyp.type_name}'
            filename = f'{item_name}.json'
            # Create Recipe keys and objects
            key = material_keys[mat.name]
            pattern = tool_patterns[ttyp.name]
            # Create json obj to make interpolation easier
            json_obj = {
                "type": "minecraft:crafting_shaped",
                "category": "misc",
                "group": f"{ttyp.name}",
                "key": key,
                "pattern": pattern,
                "result": {
                    "count": 1,
                    "id": f"minecraft:{mat.item_override_pre}_{ttyp.item_override_suf}",
                    "components": {
                        "minecraft:custom_model_data": (mat.item_model_pre * 100) + (ttyp.item_model_suf),
                        "minecraft:item_name": f"{item_name}",
                        "minecraft:custom_name": f"{custom_name}"
                    }
                },
                "show_notification": False
            }
            text = json.dumps(json_obj, indent=2)
            # Write the text to opened file
            with open(filename, 'w') as file:
                file.write(text)
            

# Prompt 
print("Confirm Creation of New files? This will overwrite old files.")
print(f"Will Create {len(materials) * len(tool_types)} tool combinations.")
print("Proceed (y/n) . . .")
answer = input()

# Input
if answer == "y":
    print("Ok")
    create_weapon_recipe_files() 