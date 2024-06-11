import os 
import json

abspath = os.path.abspath(__file__)
dir_name = os.path.dirname(abspath)
os.chdir(dir_name)

melee_enchants = [
    "arcane_cell",
    "asphyxiate",
    "backstabber",
    "bane_of_the_illager",
    "bane_of_the_sea",
    "bane_of_the_swine",
    "swap",
    "buzzy_bees",
    "budding",
    "committed",
    "cull_the_weak",
    "decaying_touch",
    "douse",
    "echo",
    "exploding",
    "fearful_finisher",
    "freezing_aspect",
    "frog_fright",
    "frosty_fuse",
    "grasp",
    "gravity_well",
    "guarding_strike",
    "gust", 
    "hemorrhage",
    "illucidation",
    "rupturing_strike",
    "tar_n_dip",
    "vengeful",
    "vital",
    "void_strike",
    "whirlwind",
]

armor_enchants = [
    "antibonk",
    "beastly",
    "black_rose",
    "blurcise",
    "brawler",
    "bulwark",
    "cowardice",
    "devastating_drop",
    "fruitful_fare",
    "ignore_pain",
    "illumineye",
    "leap_frog",
    "mandiblemania",
    "molten_core",
    "opticalization",
    "potion_barrier",
    "raging_roar",
    "reckless",
    "relentless",
    "root_boots",
    "sculk_sensitive",
    "speedy_spurs",
    "sporeful",
    "squidify",
    "sslither_ssight",
    "static_socks",
    "untouchable",
    "veiled_in_shadow",
    "vigor"
]

ranged_enchants = [
    "alchemy_artillery",
    "ballistics",
    "bola_shot",
    "burst_barrage",
    "chain_reaction",
    "cluster_shot",
    "deadeye",
    "death_from_above",
    "double_tap",
    "entanglement",
    "fan_fire",
    "gale",
    "lucky_draw",
    "luxpose",
    "overcharge",
    "perpetual",
    "rain_of_arrows", 
    "ricochet",
    "sharpshooter",
    "single_out",
    "singularity_shot",
    "rend",
    "steady_aim",
    "temporal",
    "vulnerocity",
]

other_enchants = [
    "scourer", # Rod
    "wisdom_of_the_deep", # Rod
    "bomb_ob", # Rod
    "hook_shot", # Rod
    "lengthy_line", # Rod
    "yank", # Rod
    "mirror_force", # Shield
    "void_jump", # Elytra
]

misc_enchants = [
    "chitin", # ALL
    "moonpatch", # ALL
    "o_shiny", # ALL
    
    "encumbering_curse",
    "parasitic_curse"
]

# Function to create files
def create_enchantmnet_files():
    # Iterate through each list 
    for enchant in melee_enchants:
        supported = "#odyssey:enchantable/melee"
        slots = ["mainhand"]
        create_json_obj(enchant, supported, slots)
    for enchant in armor_enchants:
        supported = "#minecraft:enchantable/armor"
        slots = ["armor"]
        create_json_obj(enchant, supported, slots)
    for enchant in ranged_enchants:
        supported = "#odyssey:enchantable/ranged"
        slots = ["mainhand"]
        create_json_obj(enchant, supported, slots)
    for enchant in other_enchants:
        supported = "#minecraft:enchantable/durability"
        slots = ["mainhand"]
        create_json_obj(enchant, supported, slots)
    for enchant in misc_enchants:
        supported = "#minecraft:enchantable/durability"
        slots = ["any"]
        create_json_obj(enchant, supported, slots)
        
def create_json_obj(name: str, supported: str, slots: list):
    filename = f'{name}.json'
    json_obj = {
        "anvil_cost": 6,
        "description": {
            "translate": f"enchantment.odyssey.{name}"
        },
        "effects": {
        },
        "max_cost": {
            "base": 40,
            "per_level_above_first": 10
        },
        "max_level": 3,
        "min_cost": {
            "base": 15,
            "per_level_above_first": 10
        },
        "slots": slots,
        "supported_items": supported,
        "weight": 5
    }
    # Write to file
    #text = json.dumps(json_obj, indent=2)
    #with open(filename, 'w') as file:
    #    file.write(text)  
        
# Main
def main():
    # Prompt 
    print("Confirm Creation of New files? This will overwrite old files.")
    total_len = len(melee_enchants) + len(misc_enchants) + len(armor_enchants) + len(ranged_enchants)
    print(f"Will Create template [{total_len}] enchantment files .")
    print("Proceed (y/n) . . .")
    answer = input()
    # Input
    if answer == "y":
        print("Ok")
        create_enchantmnet_files() 
        
# Main
if __name__ == "__main__":
    main()