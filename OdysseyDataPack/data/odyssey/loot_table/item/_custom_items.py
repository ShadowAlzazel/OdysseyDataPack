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
    "grappling_hook",
    "tinkered_musket",
    "tinkered_bow",
    "auto_crossbow",
    "compact_crossbow",
    "alchemical_driver", #AKA alchemical bolter
    "explosive_arrow"
    "arcane_wand",
    "arcane_blade",
    "arcane_scepter",
    "warping_wand",
    "void_linked_kunai"
]


def file_checker():
    for item in CUSTOM_ITEMS:
        file_path = f'{item}.json'
        if not os.path.exists(file_path):
            print(f'WARNING: The file for [{item}] does not exist!')