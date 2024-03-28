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
    
    
@dataclass(frozen=True, order=True)
class ToolType: 
    name: str = 'weapon'  # 'item_name' component
    type_name: str = 'Custom Tool' # 'custom_name' component
    base_damage: int = 0
    base_speed: int = 1.0
    item_model_suf: int = 67 # 'custom_model_data' compnent [XXXXX67]
    item_override_suf: str = 'sword' # for finding the item id
    #pattern: list[str] = field(default_factory=list)

materials = [
    Material('iron', 'Iron', 3.0, 69057, 'iron'),
    Material('diamond', 'Diamond', 4.0, 69057, 'diamond')
    #Material('titanium', 'Titanium', 4.0, 69068),
    #Material('andonized_titanium', 'Andonized Titanium', 4.0, 69070)
]
    
tool_types = [
    ToolType('katana', 'Katana', 4.0, 1.5, 44, 'sword'),
    ToolType('claymore', 'Claymore', 7.0, 0.85, 45, 'sword')
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
    ]
} 

# Add way to ovveride 
material_keys = {
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
    }
}