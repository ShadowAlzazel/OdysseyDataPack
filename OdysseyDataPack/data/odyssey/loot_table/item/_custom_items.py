import os 
import json
import math

abspath = os.path.abspath(__file__)
dir_name = os.path.dirname(abspath)
os.chdir(dir_name)

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------


CUSTOM_ITEMS = [
    # Exotics
    "abzu_blade",
    "elucidator",
    "excalibur",
    "knight_breaker",
    "shogun_lightning",
    "frost_fang",
    # Pet Food
    "dog_spinach",
    "dog_sizzle_crisp",
    "dog_milk_bone",
    # Misc Items
    "sculk_pointer",
    "totem_of_vexing",
    "irradiated_fruit",
    "sculk_heart",
    "soul_omamori",
    "soul_spice"
    # Equipment
    "titanium_musket",
    "auto_crossbow"
]


def file_checker():
    global CUSTOM_ITEMS
    for item in CUSTOM_ITEMS:
        file_path = f'{item}.json'
        if not os.path.exists(file_path):
            print(f'WARNING: The file for [{item}] does not exist!')


# Main
def main():
    # Prompt 
    print("This will check if these items exist.")
    print("Proceed (y/n) . . .")
    answer = input()
    # Input
    if answer == "y":
        print("Ok")
        file_checker() 
        
# Main
if __name__ == "__main__":
    main()