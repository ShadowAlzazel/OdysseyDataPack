import os 
import json
from dataclasses import dataclass, field

abspath = os.path.abspath(__file__)
dir_name = os.path.dirname(abspath)
os.chdir(dir_name)

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

@dataclass(frozen=True, order=True)
class Material: 
    name: str = 'material' # 'item_name' component
    full_name: str = 'Custom Material' # 'custom_name' component
    bonus_damage: int = 0
    item_override_pre: str = 'stone' # for finding the item id
    max_durability: int = None
    
    
@dataclass(frozen=True, order=True)
class ToolType: 
    name: str = 'weapon'  # 'item_name' component
    full_name: str = 'Custom Tool' # 'custom_name' component
    base_damage: int = 0
    base_speed: int = 1.0
    item_override_suf: str = 'sword' # for finding the item id

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

TOOL_MATERIALS: list[Material] = [
    # Minecraft
    Material('wooden', 'Wooden', 1.0, 'wooden'),
    Material('golden', 'Golden', 1.5, 'golden'),
    Material('stone', 'Stone', 2.0, 'stone'),
    Material('iron', 'Iron', 3.0, 'iron'),
    Material('diamond', 'Diamond', 4.0, 'diamond'),
    # Odyssey
    Material('copper', 'Copper', 2.5, 'golden', 198),
    #Material('silver', 'Silver', 3.0, 'iron', 231),
    #Material('soul_steel', 'Soul Steel', 4.0, 'iron', 666),
    #Material('titanium', 'Titanium', 4.0, 'iron', 1002),
    #Material('anodized_titanium', 'anodized Titanium', 4.0, 'iron', 1002),
    #Material('iridium', 'Iridium', 4.0, 'iron', 3108),
    #Material('mithril', 'Mithril', 4.0, 'iron', 17)
]
    
TOOL_TYPES: list[ToolType] = [
    ToolType('katana', 'Katana', 4.0, 1.8, 'sword'),
    ToolType('longsword', 'Longsword', 4.0, 1.5, 'sword'),
    #ToolType('claymore', 'Claymore', 7.0, 0.85, 'sword'),
    #ToolType('dagger', 'Dagger', 1.0, 3.0, 'sword')
]

# Create pattern
TOOL_CRAFTING_PATTERNS = {
    'katana': [
        "  X",
        "CX ",
        "#  "
    ],
    'claymore': [
        " X ",
        "XXX",
        " # "
    ],
    'dagger': [
        " X",
        "# "
    ],
    'longsword': [
        "  X",
        " X ",
        "#  "
    ]
} 

# "X" is the main ingredient and "#" is the main stick
MATERIAL_KEYS = {
    # Minecraft
    'wooden': {
        "X": "#minecraft:planks",
        "#": "minecraft:stick"
    },
    'stone': {
        "X": "minecraft:cobblestone",
        "#": "minecraft:stick"
    },
    'golden': {
        "X": "minecraft:gold_ingot",
        "#": "minecraft:stick"
    },
    'iron': {
        "X": "minecraft:iron_ingot",
        "#": "minecraft:stick"
    },
    'diamond': {
        "X": "minecraft:diamond",
        "#": "minecraft:stick"
    },
    # Odyssey
    'copper': {
        "X": "minecraft:copper_ingot",
        "#": "minecraft:stick"
    }
}

# "C" is for the complementary ingredient
TOOL_SPECIFIC_KEYS = {
    'katana': {
        "C": "minecraft:copper_ingot",
    }
}

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

# Helper function to create modifier objects
def create_modifier_obj(attribute: str, slot: str, name: str, amount: float=1.0, operation: str="add_value"):
    modifier = {
        "type": attribute,
        "slot": slot,
        "id": f'odyssey:{name}',
        "amount": amount,
        "operation": operation
    }
    return modifier


def create_modifier_list(damage: float, speed: float):
    # Lambda funcs for generic modifiers
    basic_attack_damage = lambda a : create_modifier_obj(
        attribute="minecraft:attack_damage",
        slot="mainhand",
        name="item.attack_damage",
        amount=a
    )
    reset_attack_speed = create_modifier_obj(
        attribute="minecraft:attack_speed",
        slot="mainhand",
        name="item.reset_attack_speed",
        amount=-4.0
    )
    basic_attack_speed = lambda a : create_modifier_obj(
        attribute="minecraft:attack_speed",
        slot="mainhand",
        name="item.attack_speed",
        amount=a
    )
    modifiers = [
        basic_attack_damage(damage),
        reset_attack_speed,
        basic_attack_speed(speed)
    ]
    return modifiers

# TODO 
# Add [double_axe(labrys)]
# Rework [Rapier], [Lance]

# Function to create weapon recipe files 
def create_recipe_file(material: Material, tool: ToolType): 
    # Create variables for names
    item_name = f'{material.name}_{tool.name}'
    custom_name = f"{{\"text\": \"{material.full_name} {tool.full_name}\", \"italic\": {False}}}"
    filename = f'{item_name}.json'
    # Create Recipe keys and objects
    crafting_keys = MATERIAL_KEYS[material.name] 
    tk = TOOL_SPECIFIC_KEYS.get(tool.name)
    if tk != None: # Merge if find key
        crafting_keys = crafting_keys | tk
    pattern = TOOL_CRAFTING_PATTERNS[tool.name]
    # Get stats and attributes
    damage = material.bonus_damage + tool.base_damage
    speed = tool.base_speed
    modifiers = create_modifier_list(damage, speed)
    model_data = {"strings":[tool.name,"blade","handle","hilt","pommel","no_trim"]}
    # Create Components obj
    components = {
        "minecraft:item_model": f'odyssey:{item_name}',
        "minecraft:custom_model_data": model_data,
        "minecraft:item_name": item_name,
        "minecraft:custom_name": custom_name,
        "minecraft:attribute_modifiers": modifiers
    }
    if material.max_durability != None:
        components["minecraft:max_damage"] = material.max_durability
    # Assemble json obj 
    item_override = f'minecraft:{material.item_override_pre}_{tool.item_override_suf}'
    json_obj = {
        "type": "minecraft:crafting_shaped",
        "category": "equipment",
        "group": f'{tool.name}',
        "key": crafting_keys,
        "pattern": pattern,
        "result": {
            "count": 1,
            "id": item_override,
            "components": components
        },
        "show_notification": True
    }
    # Write
    text = json.dumps(json_obj, indent=2)
    with open(filename, 'w') as file:
        file.write(text)
            

def populate_files():
    for tool in TOOL_TYPES:
        for mat in TOOL_MATERIALS:
            create_recipe_file(mat, tool)


# Main
def main():
    # Prompt 
    print("Confirm Creation of New files? This will overwrite old files.")
    print(f"Will Create {len(TOOL_TYPES) * len(TOOL_MATERIALS)} tool items.")
    print("Proceed (y/n) . . .")
    answer = input()
    # Input
    if answer == "y":
        print("Ok")
        populate_files() 
        
# Main
if __name__ == "__main__":
    main()