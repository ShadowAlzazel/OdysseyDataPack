import os 
import json

from _weapon_data import *

abspath = os.path.abspath(__file__)
dir_name = os.path.dirname(abspath)
os.chdir(dir_name)

# Helper function to create modifier objects
def create_modifier_obj(typ, slot, uuid, name, amount, operation):
    modifier = {
        "type": typ,
        "slot": slot,
        "uuid": uuid,
        "name": name,
        "amount": amount,
        "operation": operation
    }
    return modifier

def create_modifier_list(damage, speed):
    # Lambda funcs for generic modifiers
    basic_attack_damage = lambda a : create_modifier_obj(
        "minecraft:generic.attack_damage",
        "mainhand",
        [2,2,2,2],
        "odyssey:generic.attack_damage",
        a,
        "add_value"
    )
    #global reset_attack_speed FIX TO ONLY USE 
    reset_attack_speed = create_modifier_obj(
        "minecraft:generic.attack_speed",
        "mainhand",
        [1,1,1,3],
        "odyssey:generic.attack_speed",
        -4,
        "add_value"
    )
    #print(hex(id(reset_attack_speed)))
    basic_attack_speed = lambda a : create_modifier_obj(
        "minecraft:generic.attack_speed",
        "mainhand",
        [1,1,1,4],
        "odyssey:generic.attack_speed",
        a,
        "add_value"
    )
    #print(f'Damage for {filename}: {basic_attack_damage(damage)}')
    modifiers = [
        basic_attack_damage(damage),
        reset_attack_speed,
        basic_attack_speed(speed)
    ]
    return modifiers