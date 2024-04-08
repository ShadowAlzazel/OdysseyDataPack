import os 
import json
from dataclasses import dataclass, field

abspath = os.path.abspath(__file__)
dir_name = os.path.dirname(abspath)
os.chdir(dir_name)

@dataclass(frozen=True, order=True)
class Material: 
    name: str = 'material' # 'item_name' component
    material_name: str = 'Custom Material' # 'custom_name' component
    mat_damage: int = 0
    item_model_pre: int = 12345 # 'custom_model_data' component [12345XX]
    item_override_pre: str = 'stone' # for finding the item id
    max_durability: int = None
    
    
@dataclass(frozen=True, order=True)
class ToolType: 
    name: str = 'weapon'  # 'item_name' component
    tool_name: str = 'Custom Tool' # 'custom_name' component
    base_damage: int = 0
    base_speed: int = 1.0
    item_model_suf: int = 67 # 'custom_model_data' compnent [XXXXX67]
    item_override_suf: str = 'sword' # for finding the item id

materials = [
    # Minecraft
    Material('wooden', 'Wooden', 1.0, 69057, 'wooden'),
    Material('golden', 'Golden', 1.5, 69057, 'golden'),
    Material('stone', 'Stone', 2.0, 69057, 'stone'),
    Material('iron', 'Iron', 3.0, 69057, 'iron'),
    Material('diamond', 'Diamond', 4.0, 69057, 'diamond'),
    # Odyssey
    Material('copper', 'Copper', 2.5, 69055, 'golden', 198),
    #Material('silver', 'Silver', 3.0, 69063, 'iron', 231),
    #Material('soul_steel', 'Soul Steel', 4.0, 69066, 'iron', 666),
    #Material('titanium', 'Titanium', 4.0, 69068, 'iron', 1002),
    #Material('andonized_titanium', 'Andonized Titanium', 4.0, 69070, 'iron', 1002),
    #Material('iridium', 'Iridium', 4.0, 69071, 'iron', 3108),
    #Material('mithril', 'Mithril', 4.0, 69076, 'iron', 17)
]
    
tool_types = [
    ToolType('katana', 'Katana', 4.0, 1.5, 44, 'sword'),
    ToolType('claymore', 'Claymore', 7.0, 0.85, 45, 'sword'),
    ToolType('dagger', 'Dagger', 1.0, 3.0, 46, 'sword')
]

# Create pattern
tool_patterns = {
    'katana': [
        "  X",
        "CX ",
        "|  "
    ],
    'claymore': [
        " X ",
        "XXX",
        " | "
    ],
    'dagger': [
        " X",
        "| "
    ]
} 

# "X" is the main ingredient and "|" is the main stick
material_keys = {
    # Minecraft
    'wooden': {
        "X": {"tag": "minecraft:planks"},
        "|": {"item": "minecraft:stick"}
    },
    'stone': {
        "X": {"item": "minecraft:cobblestone"},
        "|": {"item": "minecraft:stick"}
    },
    'golden': {
        "X": {"item": "minecraft:gold_ingot"},
        "|": {"item": "minecraft:stick"}
    },
    'iron': {
        "X": {"item": "minecraft:iron_ingot"},
        "|": {"item": "minecraft:stick"}
    },
    'diamond': {
        "X": {"item": "minecraft:diamond"},
        "|": {"item": "minecraft:stick"}
    },
    # Odyssey
    'copper': {
        "X": {"item": "minecraft:copper_ingot"},
        "|": {"item": "minecraft:stick"}
    },
    'mithril': {
        "X": {"item": "minecraft:copper_ingot"},
        "|": {"item": "minecraft:stick"}
    },
}

# "C" is for the complementary ingredient
tool_keys = {
    'katana': {
        "C": {"item": "minecraft:copper_ingot"},
    }
}