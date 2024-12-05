import os 
import json
import math
from dataclasses import dataclass, field
from typing import Optional, Union, Dict

from _item_maker import *
from _custom_items import file_checker

abspath = os.path.abspath(__file__)
dir_name = os.path.dirname(abspath)
os.chdir(dir_name)

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

ITEMS = [
    # Ingredients
    ItemData("arcane_book", "book"),
    ItemData("anodized_titanium_ingot", "iron_ingot"),
    ItemData("coagulated_blood", "rotten_flesh"),
    ItemData("ectoplasm", "rotten_flesh"),
    ItemData("heated_titanium_ingot", "iron_ingot"),
    ItemData("iridium_ingot", "iron_ingot"),
    ItemData("blank_tome", "book"),
    ItemData("alexandrite", "emerald"),
    ItemData("jade", "emerald"),
    ItemData("jovianite", "emerald"),
    ItemData("kunzite", "emerald"),
    ItemData("mithril_ingot", "iron_ingot"),
    ItemData("neptunian", "emerald"),
    ItemData("ruby", "emerald"),
    ItemData("silver_ingot", "iron_ingot"),
    ItemData("silver_nugget", "iron_nugget"),
    ItemData("soul_steel_ingot", "iron_ingot"),
    ItemData("titanium_ingot", "iron_ingot"),
    ItemData("shadow_trial_key", "trial_key"),
    # Smithing
    ItemData("imperial_armor_trim_smithing_template", "paper"),
    ItemData("voyager_armor_trim_smithing_template", "paper"),
    ItemData("leaf_armor_trim_smithing_template", "paper"),
    ItemData("danger_armor_trim_smithing_template", "paper"),
    ItemData("ring_armor_trim_smithing_template", "paper"),
    ItemData("cross_weapon_trim_smithing_template", "paper"),
    ItemData("spine_weapon_trim_smithing_template", "paper"),
    ItemData("wings_weapon_trim_smithing_template", "paper"),
    ItemData("trace_weapon_trim_smithing_template", "paper"),
    ItemData("jewel_weapon_trim_smithing_template", "paper"),
    ItemData("mithril_upgrade_template", "paper"),
    ItemData("soul_steel_upgrade_template", "paper"),
    ItemData("titanium_upgrade_template", "paper"),
    ItemData("iridium_upgrade_template", "paper"),
    # Enchanting
    ItemData("tome_of_discharge", "paper"),
    ItemData("tome_of_expenditure", "paper"),
    ItemData("tome_of_extraction", "paper"),
    ItemData("tome_of_imitation", "paper"),
    ItemData("tome_of_promotion", "paper"),
    ItemData("tome_of_avarice", "paper"),
    ItemData("tome_of_harmony", "paper"),
    ItemData("tome_of_replication", "paper"),
    # Tool Parts
    ItemData("blade_part_upgrade_template", "paper"),
    ItemData("handle_part_upgrade_template", "paper"),
    ItemData("pommel_part_upgrade_template", "paper"),
    ItemData("hilt_part_upgrade_template", "paper"),
    ItemData("empty_part_upgrade_template", "paper"),
    ItemData("voyager_part_pattern", "paper"),
    ItemData("danger_part_pattern", "paper"),
    ItemData("seraph_part_pattern", "paper"),
    ItemData("marauder_part_pattern", "paper"),
    ItemData("crusader_part_pattern", "paper"),
    ItemData("vandal_part_pattern", "paper"),
    ItemData("imperial_part_pattern", "paper"),
    ItemData("fancy_part_pattern", "paper"),
    ItemData("humble_part_pattern", "paper"),
    ItemData("empty_part_pattern", "paper"),
    # Glyphic
    ItemData("glazed_orb", "brick"),
    ItemData("glazed_rods", "brick"), 
    ItemData("glazed_key", "brick"), 
    ItemData("glazed_skull", "brick"), 
    ItemData("glazed_dowel", "brick"), 
    ItemData("glazed_totem", "brick"), 
    ItemData("clay_orb", "clay_ball"),
    ItemData("clay_rods", "clay_ball"), 
    ItemData("clay_key", "clay_ball"), 
    ItemData("clay_skull", "clay_ball"), 
    ItemData("clay_dowel", "clay_ball"), 
    ItemData("clay_totem", "clay_ball"), 
    # Glyphsherds
    ItemData("assault_glyphsherd", "brick",[AttributesComponent([Modifier("attack_damage", 1, "mainhand", "glyph.slot")])]),
    ItemData("guard_glyphsherd", "brick",[AttributesComponent([Modifier("armor", 1, "armor", "glyph.slot")])]),
    ItemData("finesse_glyphsherd", "brick",[AttributesComponent([Modifier("attack_speed", 0.2, "armor", "glyph.slot")])]),
    ItemData("swift_glyphsherd", "brick",[AttributesComponent([Modifier("movement_speed", 0.02, "armor", "glyph.slot")])]),
    ItemData("vitality_glyphsherd", "brick",[AttributesComponent([Modifier("max_health", 2.0, "armor", "glyph.slot")])]),
    ItemData("steadfast_glyphsherd", "brick",[AttributesComponent([Modifier("knockback_resistance", 0.2, "armor", "glyph.slot")])]),
    ItemData("force_glyphsherd", "brick",[AttributesComponent([Modifier("attack_knockback", 0.5, "mainhand", "glyph.slot")])]),
    ItemData("break_glyphsherd", "brick",[AttributesComponent([Modifier("block_break_speed", 0.5, "mainhand", "glyph.slot")])]),
    ItemData("grasp_glyphsherd", "brick",[AttributesComponent([Modifier("block_interaction_range", 1.0, "mainhand", "glyph.slot")])]),
    ItemData("jump_glyphsherd", "brick",[AttributesComponent([Modifier("jump_strength", 0.3, "armor", "glyph.slot")])]),
    ItemData("gravity_glyphsherd", "brick",[AttributesComponent([Modifier("gravity", -0.01, "armor", "glyph.slot")])]),
    ItemData("range_glyphsherd", "brick",[AttributesComponent([Modifier("entity_interaction_range", 0.5, "mainhand", "glyph.slot")])]),
    ItemData("size_glyphsherd", "brick",[AttributesComponent([Modifier("scale", 0.25, "armor", "glyph.slot")])]),
    # Food
    ItemData("bacon", "cooked_porkchop",[FoodComponent(8.0, 3, 1.2)]),
    ItemData("berry_tart", "cookie",[FoodComponent(5.5, 3, 1.6)]),
    ItemData("green_apple", "apple",[FoodComponent(5.5, 3, 1.6)]),
    ItemData("coffee", "cookie",[FoodComponent(4.0, 2, 0.8)]),
    ItemData("crystal_candy", "cookie",[FoodComponent(5.0, 2, 0.8)]),
    ItemData("fruit_bowl", "apple",[FoodComponent(12.0, 9, 2.0)]),
    ItemData("chocolate_mochi", "cookie",[FoodComponent(5.5, 3, 0.8)]),
    ItemData("fish_n_chips", "cooked_cod",[FoodComponent(13.0, 8, 1.6)]),
    ItemData("french_toast", "apple",[FoodComponent(6.0, 6, 1.6)]),
    ItemData("earl_lily_boba_tea", "cookie",[FoodComponent(5.0, 2, 0.8)]),
    ItemData("spider_eye_boba", "spider_eye",[FoodComponent(3.0, 1, 0.8)]),
    ItemData("salmon_roll", "cooked_salmon",[FoodComponent(6.0, 4, 1.2)]),
    ItemData("salmon_nigiri", "salmon",[FoodComponent(6.0, 4, 1.2)]),
    ItemData("brisket", "beef",[FoodComponent(2.0, 1, 0.8)]),
    ItemData("cooked_brisket", "cooked_beef",[FoodComponent(5.0, 3, 0.8)]),
    ItemData("shoyu_ramen", "cooked_chicken",[FoodComponent(12.0, 9, 2.0)]),
    ItemData("tonkotsu_ramen", "cooked_porkchop",[FoodComponent(14.0, 10, 2.0)]),
    ItemData("thai_tulip_boba_tea", "cookie",[FoodComponent(5.0, 2, 0.8)]),
    ItemData("matcha_melon_boba_tea", "cookie",[FoodComponent(5.0, 2, 0.8)]),
    ItemData("oolong_orchid_boba_tea", "cookie",[FoodComponent(5.0, 2, 0.8)]),
    ItemData("allium_jade_boba_tea", "cookie",[FoodComponent(5.0, 2, 0.8)]),
    ItemData("cornflower_ceylon_boba_tea", "cookie",[FoodComponent(5.0, 2, 0.8)])
]

# List
ARMOR_PIECES = ['helmet', 'chestplate', 'leggings', 'boots']
ARMOR_MATERIALS = ['silver', 'copper', 'soul_steel', 'titanium', 'anodized_titanium', 'iridium', 'mithril']


# Main
def main():
    # Run 
    create_new_item_files(ITEMS)
    create_armor_files(ARMOR_MATERIALS, ARMOR_PIECES)
    # Check
    file_checker()
    # Kotlin .txt
    to_text_line = lambda x : f'val {x.item_name.upper()} = DataItem("{x.item_name}") \n'
    lines = [to_text_line(x) for x in ITEMS]
    with open("_kotlin.txt", 'w') as f:
        f.writelines(lines)
        
# Main
if __name__ == "__main__":
    main()