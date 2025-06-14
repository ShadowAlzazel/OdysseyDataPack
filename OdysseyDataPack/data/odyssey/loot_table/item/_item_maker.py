import os 
import json
import math
from dataclasses import dataclass, field
from typing import Optional, Union, Dict, List

from _item_data import *

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

@dataclass
class DataItem:
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
class MaxDamageComponent:
    max_damage: int
    
@dataclass
class EquippableComponent:
    asset_id: str
    slot: str
    
@dataclass
class AttributesComponent:
    modifiers: list = field(default_factory=list)
    
# --------------------------------------------------------------------------

@dataclass
class Modifier:
    attribute: str
    amount: str
    slot: str
    keyId: str
    operation: str="add_value"    
    
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
        elif isinstance(x, MaxDamageComponent):
            components["minecraft:max_damage"] = x.max_damage
    # Merge    
    components_obj = {
        "function": "minecraft:set_components",
        "components": components,
        "conditions": []
    }
    # Finish 
    return components_obj                

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

def new_modifier_list(modifiers: list[Modifier]):
    modifier_list = []
    for x in modifiers:
        obj = {
            "attribute": f'minecraft:{x.attribute}',
            "operation": x.operation,
            "amount": x.amount,
            "id": f'odyssey:{x.keyId}',
            "slot": x.slot
        }
        modifier_list.append(obj)
    return modifier_list


# Basic Loot/Item Json 
def create_item_obj(item_data: DataItem) -> dict:
    # First obj to make
    override_item = f'minecraft:{item_data.item_override}'
    item_json = {
        "type": "chest",
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
    # Set Attributes
    for x in item_components:
        if isinstance(x, AttributesComponent):   
            set_attributes = {
                "function": "minecraft:set_attributes",
                "modifiers": new_modifier_list(x.modifiers)
            }
            functions.append(set_attributes)
    # Merge
    item_json["pools"][0]["entries"][0]["functions"] = functions
    # Finish
    return item_json

# --------------------------------------------------------------------------


def generate_item_file(item_data: DataItem, override_existing: bool = True) -> None:
    file_name = f'{item_data.item_name}.json'
    file_exists = os.path.isfile(file_name)
    if not file_exists or override_existing:
        item = json.dumps(create_item_obj(item_data), indent=2)
        with open(file_name, 'w') as f:
            f.write(item)
    return


def create_new_item_files(item_list: List[DataItem], override_existing: bool = True) -> None:
    # Prompt 
    if override_existing:
        print("Confirm creation of new files? This will overwrite old files!")
    else: 
        print("Confirm creation of new files? ONLY new files will be created.")
    
    #print(f"Will create {len(item_list)} items.")
    print("Proceed (y/n) . . .")
    answer = input()
    # Input
    if answer == "y":
        print("Starting generation of items...")
        for x in item_list:
            generate_item_file(x, override_existing)
        print("Finished generating item files.")
    else:
        print("Exiting...")
    return


def generate_new_armor_file(material: str, armor_piece: str):
    # Get Data
    item_name = f'{material}_{armor_piece}'
    slot = f'{BODY_SLOT_MAP[armor_piece]}'
    index = PIECE_INDEX[armor_piece]
    armor_val = ARMOR_VALUES[material][index]
    toughness_val = TOUGHNESS_VALUES[material][index]
    durability_val = int(BASE_ARMOR_DURABILITY[index] * DURABILITY_VALUES[material])
    keyId = f'item.{armor_piece}'
    # Create DataItem
    modifiers = [
        Modifier("armor", armor_val, slot, f'{keyId}.armor'),
        Modifier("armor_toughness", toughness_val, slot, f'{keyId}.armor_toughness')
    ]
    override_item = f'iron_{armor_piece}'

    components = [
        AttributesComponent(modifiers),
        EquippableComponent(material, slot),
        MaxDamageComponent(durability_val)
    ]
    data = DataItem(item_name, override_item, components)
    # Create file
    generate_item_file(data)   


def create_armor_files(materials: list[str], pieces: list[str]) -> None:
    for material in materials:
        for armor_piece in pieces:
            generate_new_armor_file(material, armor_piece)