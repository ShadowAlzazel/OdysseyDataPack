import os 
import json

from _weapon_data import *
from _modifier_data import *

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
    # Loop for all combinations
    for i in range(len(materials)):
        for j in range(len(tool_types)):
            mat: Material = materials[i]
            ttyp: ToolType = tool_types[j]
            # Creating seperate parts to fit in json obj to make interpolation easier
            # -----------------------------------------------------------------------
            # Create variables for names
            item_name = f'{mat.name}_{ttyp.name}'
            custom_name = f"{{\"text\": \"{mat.material_name} {ttyp.tool_name}\", \"italic\": {False}}}"
            filename = f'{item_name}.json'
            damage = mat.mat_damage + ttyp.base_damage
            speed = ttyp.base_speed
            # Create Recipe keys and objects
            key = material_keys[mat.name] 
            tk = tool_keys.get(ttyp.name)
            if tk != None: # Merge if find key
                key = key | tk
            # Get Pattern from keys
            pattern = tool_patterns[ttyp.name]
            # Create Modifiers
            modifiers = create_modifier_list(damage, speed)
            # Create Components
            components = {
                "minecraft:custom_model_data": (mat.item_model_pre * 100) + (ttyp.item_model_suf),
                "minecraft:item_name": f"{item_name}",
                "minecraft:custom_name": f"{custom_name}",
                "minecraft:attribute_modifiers": modifiers
            }
            if mat.max_durability != None:
                components["minecraft:max_damage"] = mat.max_durability

            # -----------------
            # Assemble json obj 
            json_obj = {
                "type": "minecraft:crafting_shaped",
                "category": "equipment",
                "group": f"{ttyp.name}",
                "key": key,
                "pattern": pattern,
                "result": {
                    "count": 1,
                    "id": f"minecraft:{mat.item_override_pre}_{ttyp.item_override_suf}",
                    "components": components
                },
                "show_notification": True
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