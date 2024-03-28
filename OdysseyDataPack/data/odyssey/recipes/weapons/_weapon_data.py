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
    item_model_pre: int = 12345 # 'custom_model_data' compnent [12345XX]
    item_override_pre: str = 'diamond' # for finding the item id
    max_durability: int = None
    
    
@dataclass(frozen=True, order=True)
class ToolType: 
    name: str = 'weapon'  # 'item_name' component
    tool_name: str = 'Custom Tool' # 'custom_name' component
    base_damage: int = 0
    base_speed: int = 1.0
    item_model_suf: int = 67 # 'custom_model_data' compnent [XXXXX67]
    item_override_suf: str = 'sword' # for finding the item id
    #pattern: list[str] = field(default_factory=list)

materials = [
    # Minecraft
    Material('golden', 'Golden', 1.5, 69057, 'golden'),
    Material('iron', 'Iron', 3.0, 69057, 'iron'),
    Material('diamond', 'Diamond', 4.0, 69057, 'diamond'),
    # Odyssey
    Material('copper', 'Copper', 2.5, 69055, 'golden', 158)
    #Material('titanium', 'Titanium', 4.0, 69068),
    #Material('andonized_titanium', 'Andonized Titanium', 4.0, 69070)
]
    
tool_types = [
    ToolType('katana', 'Katana', 4.0, 1.5, 44, 'sword'),
    ToolType('claymore', 'Claymore', 7.0, 0.85, 45, 'sword'),
    ToolType('dagger', 'Dagger', 1.0, 3.0, 46, 'sword')
]


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

# Add way to ovveride 
material_keys = {
    'wooden': {
        "X": {"tag": "minecraft:planks"},
        "|": {"item": "minecraft:stick"}
    },
    'stone': {
        "X": {"item": "minecraft:gold_ingot"},
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
    'copper': {
        "X": {"item": "minecraft:copper_ingot"},
        "|": {"item": "minecraft:stick"}
    },
}

tool_keys = {
    'katana': {
        "C": {"item": "minecraft:copper_ingot"},
    }
}