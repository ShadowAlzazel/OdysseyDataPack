import os 
import json
import math
from dataclasses import dataclass, field
from typing import Optional, Union, Dict

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

@dataclass
class ItemData:
    item_name: str
    item_override: str
    components: list = field(default_factory=list)

# --------------------------------------------------------------------------

@dataclass()
class ItemNameComponent:
    item_name: str
  
@dataclass  
class ItemModelComponent:
    item_model: str

@dataclass
class FoodComponent:
    saturation: float
    nutrition: int
    consume_seconds: Optional[float]=None
    can_always_eat: bool=False
    
@dataclass
class ConsumableComponent:
    consume_seconds: float=2.4
    
@dataclass
class EquippableComponent:
    asset_id: str
    slot: str
    
# --------------------------------------------------------------------------

def get_components_obj(data_components: list):
    namespace = "odyssey"
    components = {}
    for x in data_components:
        if isinstance(x, FoodComponent):
            if x.consume_seconds: # Checks if too add consumable component
                temp_consumable = ConsumableComponent(x.consume_seconds)
                components["minecraft:consumable"] = new_consumable_component(temp_consumable)
            components["minecraft:food"] = new_food_component(x)
        elif isinstance(x, EquippableComponent):
            components["minecraft:equippable"] = new_equippable_component(x)
        elif isinstance(x, ItemModelComponent):
            components["minecraft:item_model"] = f'{namespace}:{x.item_model}'
        elif isinstance(x, ItemNameComponent):
            components["minecraft:item_name"] = x.item_name
    # Merge    
    components_obj = {
        "function": "minecraft:set_components",
        "components": components,
        "conditions": []
    }
    # Finish 
    return components_obj
        
# --------------------------------------------------------------------------                

def new_food_component(component: FoodComponent):
    return {
        "nutrition": int(component.nutrition),
        "saturation": float(component.saturation),
        "can_always_eat": component.can_always_eat
    }


def new_equippable_component(component: EquippableComponent):
    return {
        "asset_id": f'odyssey:{component.asset_id}',
        "slot": component.slot,
        "equip_sound": "item.armor.equip_chain"
    }


def new_consumable_component(component: ConsumableComponent):
    return {
        "consume_seconds": float(component.consume_seconds)
    }


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

# Basic Loot/Item Json 
def create_item_obj(item_data: ItemData) -> dict:
    # First obj to make
    override_item = f'minecraft:{item_data.item_override}'
    item_json = {
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
    # Function jsons
    functions = []
    # Set Components
    item_components = item_data.components
    item_components.insert(0, ItemNameComponent(item_data.item_name))
    item_components.insert(1, ItemModelComponent(item_data.item_name))
    set_components = get_components_obj(item_components)
    functions.append(set_components)
    # Set Name
    set_name = {
        "function": "minecraft:set_name",
        "entity": "this",
        "name": {
            "text": f'{item_data.item_name}'.replace("_", " ").title(),
            "bold": False,
            "italic": False
        }
    } 
    functions.append(set_name)
    # Merge
    item_json["pools"][0]["entries"][0]["functions"] = functions
    # Finish
    return item_json


def generate_item_file(item_data: ItemData) -> None:
    file_name = f'{item_data.item_name}.json'
    item = json.dumps(create_item_obj(item_data), indent=2)
    with open(file_name, 'w') as f:
        f.write(item)
    return

def populate_files(item_list: [ItemData]) -> None:
    # Prompt 
    print("Confirm creation of new files? This will overwrite old files!")
    print(f"Will create {len(item_list)} items.")
    print("Proceed (y/n) . . .")
    answer = input()
    # Input
    if answer == "y":
        print("Ok")
        for x in item_list:
            generate_item_file(x)
        print("Finished generating item files.")
    else:
        print("Exiting...")
    return