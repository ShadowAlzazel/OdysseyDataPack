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
    DataItem("arcane_book", "book"),
    DataItem("arcane_pen", "bundle"),
    DataItem("anodized_titanium_ingot", "iron_ingot"),
    DataItem("coagulated_blood", "rotten_flesh"),
    DataItem("ectoplasm", "rotten_flesh"),
    DataItem("soul_quartz", "quartz"),
    DataItem("heated_titanium_ingot", "iron_ingot"),
    DataItem("iridium_ingot", "iron_ingot"),
    DataItem("blank_tome", "book"),
    DataItem("alexandrite", "emerald"),
    DataItem("jade", "emerald"),
    DataItem("jovianite", "emerald"),
    DataItem("kunzite", "emerald"),
    DataItem("mithril_ingot", "iron_ingot"),
    DataItem("neptunian", "emerald"),
    DataItem("ruby", "emerald"),
    DataItem("silver_ingot", "iron_ingot"),
    DataItem("silver_nugget", "iron_nugget"),
    DataItem("soul_steel_ingot", "iron_ingot"),
    DataItem("titanium_ingot", "iron_ingot"),
    DataItem("shadow_trial_key", "trial_key"),
    DataItem("crystal_alloy_ingot", "iron_ingot"),
    # Smithing
    DataItem("imperial_armor_trim_smithing_template", "paper"),
    DataItem("voyager_armor_trim_smithing_template", "paper"),
    DataItem("leaf_armor_trim_smithing_template", "paper"),
    DataItem("danger_armor_trim_smithing_template", "paper"),
    DataItem("ring_armor_trim_smithing_template", "paper"),
    DataItem("cross_weapon_trim_smithing_template", "paper"),
    DataItem("spine_weapon_trim_smithing_template", "paper"),
    DataItem("wings_weapon_trim_smithing_template", "paper"),
    DataItem("trace_weapon_trim_smithing_template", "paper"),
    DataItem("jewel_weapon_trim_smithing_template", "paper"),
    DataItem("mithril_upgrade_template", "paper"),
    DataItem("soul_steel_upgrade_template", "paper"),
    DataItem("titanium_upgrade_template", "paper"),
    DataItem("iridium_upgrade_template", "paper"),
    DataItem("crystal_alloy_upgrade_template", "paper"),
    # Enchanting
    DataItem("tome_of_discharge", "enchanted_book"),
    DataItem("tome_of_expenditure", "enchanted_book"),
    DataItem("tome_of_extraction", "enchanted_book"),
    DataItem("tome_of_imitation", "enchanted_book"),
    DataItem("tome_of_promotion", "enchanted_book"),
    DataItem("tome_of_avarice", "enchanted_book"),
    DataItem("tome_of_harmony", "enchanted_book"),
    DataItem("tome_of_replication", "enchanted_book"),
    # Tool Parts
    DataItem("blade_part_upgrade_template", "gold_ingot"),
    DataItem("handle_part_upgrade_template", "gold_ingot"),
    DataItem("pommel_part_upgrade_template", "gold_ingot"),
    DataItem("hilt_part_upgrade_template", "gold_ingot"),
    DataItem("empty_part_upgrade_template", "gold_ingot"),
    DataItem("voyager_part_pattern", "paper"),
    DataItem("danger_part_pattern", "paper"),
    DataItem("seraph_part_pattern", "paper"),
    DataItem("marauder_part_pattern", "paper"),
    DataItem("crusader_part_pattern", "paper"),
    DataItem("vandal_part_pattern", "paper"),
    DataItem("imperial_part_pattern", "paper"),
    DataItem("fancy_part_pattern", "paper"),
    DataItem("humble_part_pattern", "paper"),
    DataItem("empty_part_pattern", "paper"),
    DataItem("mastercrafted_tool_template", "paper"),
    # Glyphic
    DataItem("glazed_orb", "brick"),
    DataItem("glazed_rods", "brick"), 
    DataItem("glazed_key", "brick"), 
    DataItem("glazed_skull", "brick"), 
    DataItem("glazed_dowel", "brick"), 
    DataItem("glazed_totem", "brick"), 
    DataItem("clay_orb", "clay_ball"),
    DataItem("clay_rods", "clay_ball"), 
    DataItem("clay_key", "clay_ball"), 
    DataItem("clay_skull", "clay_ball"), 
    DataItem("clay_dowel", "clay_ball"), 
    DataItem("clay_totem", "clay_ball"), 
    # Glyphsherds
    DataItem("assault_glyphsherd", "brick",[AttributesComponent([Modifier("attack_damage", 1, "mainhand", "glyph.slot")])]),
    DataItem("guard_glyphsherd", "brick",[AttributesComponent([Modifier("armor", 1, "armor", "glyph.slot")])]),
    DataItem("finesse_glyphsherd", "brick",[AttributesComponent([Modifier("attack_speed", 0.2, "armor", "glyph.slot")])]),
    DataItem("swift_glyphsherd", "brick",[AttributesComponent([Modifier("movement_speed", 0.02, "armor", "glyph.slot")])]),
    DataItem("vitality_glyphsherd", "brick",[AttributesComponent([Modifier("max_health", 2.0, "armor", "glyph.slot")])]),
    DataItem("steadfast_glyphsherd", "brick",[AttributesComponent([Modifier("knockback_resistance", 0.2, "armor", "glyph.slot")])]),
    DataItem("force_glyphsherd", "brick",[AttributesComponent([Modifier("attack_knockback", 0.5, "mainhand", "glyph.slot")])]),
    DataItem("break_glyphsherd", "brick",[AttributesComponent([Modifier("block_break_speed", 0.5, "mainhand", "glyph.slot")])]),
    DataItem("grasp_glyphsherd", "brick",[AttributesComponent([Modifier("block_interaction_range", 1.0, "mainhand", "glyph.slot")])]),
    DataItem("jump_glyphsherd", "brick",[AttributesComponent([Modifier("jump_strength", 0.3, "armor", "glyph.slot")])]),
    DataItem("gravity_glyphsherd", "brick",[AttributesComponent([Modifier("gravity", -0.01, "armor", "glyph.slot")])]),
    DataItem("range_glyphsherd", "brick",[AttributesComponent([Modifier("entity_interaction_range", 0.5, "mainhand", "glyph.slot")])]),
    DataItem("size_glyphsherd", "brick",[AttributesComponent([Modifier("scale", 0.25, "armor", "glyph.slot")])]),
    # Food
    DataItem("bacon", "cooked_porkchop",[FoodComponent(8.0, 3, 1.2)]),
    DataItem("berry_tart", "cookie",[FoodComponent(5.5, 3, 1.6)]),
    DataItem("green_apple", "apple",[FoodComponent(5.5, 3, 1.6)]),
    DataItem("coffee", "cookie",[FoodComponent(4.0, 2, 0.8)]),
    DataItem("crystal_candy", "cookie",[FoodComponent(5.0, 2, 0.8)]),
    DataItem("fruit_bowl", "apple",[FoodComponent(12.0, 9, 2.0)]),
    DataItem("chocolate_mochi", "cookie",[FoodComponent(5.5, 3, 0.8)]),
    DataItem("fish_n_chips", "cooked_cod",[FoodComponent(13.0, 8, 1.6)]),
    DataItem("french_toast", "apple",[FoodComponent(6.0, 6, 1.6)]),
    DataItem("earl_lily_boba_tea", "cookie",[FoodComponent(5.0, 2, 0.8)]),
    DataItem("spider_eye_boba", "spider_eye",[FoodComponent(3.0, 1, 0.8)]),
    DataItem("salmon_roll", "cooked_salmon",[FoodComponent(6.0, 4, 1.2)]),
    DataItem("salmon_nigiri", "salmon",[FoodComponent(6.0, 4, 1.2)]),
    DataItem("brisket", "beef",[FoodComponent(2.0, 1, 0.8)]),
    DataItem("cooked_brisket", "cooked_beef",[FoodComponent(5.0, 3, 0.8)]),
    DataItem("shoyu_ramen", "cooked_chicken",[FoodComponent(12.0, 9, 2.0)]),
    DataItem("tonkotsu_ramen", "cooked_porkchop",[FoodComponent(14.0, 10, 2.0)]),
    DataItem("thai_tulip_boba_tea", "cookie",[FoodComponent(5.0, 2, 0.8)]),
    DataItem("matcha_melon_boba_tea", "cookie",[FoodComponent(5.0, 2, 0.8)]),
    DataItem("oolong_orchid_boba_tea", "cookie",[FoodComponent(5.0, 2, 0.8)]),
    DataItem("allium_jade_boba_tea", "cookie",[FoodComponent(5.0, 2, 0.8)]),
    DataItem("cornflower_ceylon_boba_tea", "cookie",[FoodComponent(5.0, 2, 0.8)]),
    # Misc
    DataItem("explosive_arrow", "arrow"), 
    DataItem("totem_of_vexing", "arrow"), 
    DataItem("irradiated_fruit", "arrow"), 
    DataItem("sculk_heart", "arrow"), 
    DataItem("sculk_pointer", "arrow"), 
    DataItem("soul_spice", "arrow"), 
    DataItem("soul_omamori", "arrow"), 
]

CUSTOM: list[DataItem] = [
    # TEMP TODO Equipment
    DataItem("tinkered_bow", "bow"),
    DataItem("chain_hook", "crossbow"),
    DataItem("tinkered_musket", "crossbow"),
    DataItem("auto_crossbow", "crossbow"),
    DataItem("compact_crossbow", "crossbow"),
    DataItem("alchemical_driver", "crossbow"),
    DataItem("alchemical_diffuser", "crossbow"),
    DataItem("alchemical_bolter", "crossbow"),
    DataItem("arcane_wand", "stick"),
    DataItem("arcane_blade", "stick"),
    DataItem("arcane_scepter", "stick"),
    DataItem("warping_wand", "stick"),
    DataItem("void_linked_kunai", "iron_sword"),
    DataItem("scroll", "paper"),
    DataItem("spell_scroll", "paper"),
]

# List
ARMOR_PIECES = ['helmet', 'chestplate', 'leggings', 'boots']
ARMOR_MATERIALS = ['silver', 'copper', 'soul_steel', 'titanium', 'anodized_titanium', 'iridium', 'mithril', 'crystal_alloy']


# Main
def main():
    # Create item files from DataItem
    create_new_item_files(ITEMS, False)
    # Create Armor items
    create_armor_files(ARMOR_MATERIALS, ARMOR_PIECES)
    # Create basic file for CUSTOM items   
    for item in CUSTOM:
        file_path = f'{item.item_name}.json'
        if not os.path.exists(file_path):
            print(f'WARNING: The file for [{file_path}] does not exist! Creating new file.')
            generate_item_file(item)
        #generate_item_file(item) # OVERRIDE
    # Write as kotlin values -> _kotlin .txt
    ALL_ITEMS = ITEMS + CUSTOM
    to_text_line = lambda x : f'val {x.item_name.upper()} = DataItem("{x.item_name}") \n'
    lines = [to_text_line(x) for x in ALL_ITEMS]
    with open("_kotlin.txt", 'w') as f:
        f.writelines(lines)

# Main
if __name__ == "__main__":
    main()