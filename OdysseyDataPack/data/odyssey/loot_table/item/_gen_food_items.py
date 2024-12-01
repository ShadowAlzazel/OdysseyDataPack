import os 
import json
import math
from dataclasses import dataclass

abspath = os.path.abspath(__file__)
dir_name = os.path.dirname(abspath)
os.chdir(dir_name)

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

@dataclass
class FoodData:
    item_override: str 
    saturation: float
    nutrition: int
    consume_seconds: float=2.4
    can_always_eat: bool=False
    

FOOD_ITEMS: dict[str, FoodData] = {
    "bacon": FoodData("cooked_porkchop", 8.0, 3, 1.2),
    "berry_tart": FoodData("cookie", 5.5, 3, 1.6),
    "green_apple": FoodData("apple", 5.5, 3, 1.6),
    "coffee": FoodData("cookie", 4.0, 2, 0.8),
    "crystal_candy": FoodData("cookie", 5.0, 2, 0.8),
    "fruit_bowl": FoodData("apple", 12.0, 9, 2.0),
    "chocolate_mochi": FoodData("cookie", 5.5, 3, 0.8),
    "fish_n_chips": FoodData("cooked_cod", 13.0, 8, 1.6),
    "french_toast": FoodData("apple", 6.0, 6, 1.6),
    "earl_lily_boba_tea": FoodData("cookie", 5.0, 2, 0.8),
    "spider_eye_boba": FoodData("spider_eye", 3.0, 1, 0.8),
    "salmon_roll": FoodData("cooked_salmon", 6.0, 4, 1.2),
    "salmon_nigiri": FoodData("salmon", 6.0, 4, 1.2),
    "brisket": FoodData("beef", 2.0, 1, 0.8),
    "cooked_brisket": FoodData("cooked_beef", 5.0, 3, 0.8),
    "shoyu_ramen": FoodData("cooked_chicken", 12.0, 9, 2.0),
    "tonkotsu_ramen": FoodData("cooked_porkchop", 14.0, 10, 2.0),
    "thai_tulip_boba_tea": FoodData("cookie", 5.0, 2, 0.8),
    "matcha_melon_boba_tea": FoodData("cookie", 5.0, 2, 0.8),
    "oolong_orchid_boba_tea": FoodData("cookie", 5.0, 2, 0.8),
    "allium_jade_boba_tea": FoodData("cookie", 5.0, 2, 0.8),
    "cornflower_ceylon_boba_tea": FoodData("cookie", 5.0, 2, 0.8)
}

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------


# Creation Function
def create_item_file(item_name: str):
    # Create item file name
    global FOOD_ITEMS
    item_data: FoodData = FOOD_ITEMS[item_name]
    filename = f'{item_name}.json'
    override_item = f'minecraft:{item_data.item_override}'
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
            "minecraft:item_model": f'odyssey:{item_name}',
            "minecraft:consumable": {
                "consume_seconds": float(item_data.consume_seconds)
            },
            "minecraft:food": {
                "nutrition": int(item_data.nutrition),
                "saturation": float(item_data.saturation),
                "can_always_eat": item_data.can_always_eat
            }
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
    for key in FOOD_ITEMS:
        create_item_file(key)
    
# Main
def main():
    # Prompt 
    print("Confirm Creation of New files? This will overwrite old files.")
    print(f"This will Create {len(FOOD_ITEMS)} items.")
    print("Proceed (y/n) . . .")
    answer = input()
    # Input
    if answer == "y":
        print("Ok")
        populate_files() 
        
# Main
if __name__ == "__main__":
    main()