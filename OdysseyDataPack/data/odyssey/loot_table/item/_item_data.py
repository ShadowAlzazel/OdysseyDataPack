import os 
import json
import math

# --------------------------------------------------------------------------

# Maps
BODY_SLOT_MAP = {
    'helmet': 'head', 
    'chestplate': 'chest',
    'leggings': 'legs', 
    'boots': 'feet'
}
PIECE_INDEX = {
    'helmet': 0, 
    'chestplate': 1,
    'leggings': 2, 
    'boots': 3
}

# Values
ARMOR_VALUES = {
    'copper': [2, 4, 3, 1],
    'silver': [3, 5, 3, 2], 
    'soul_steel': [3, 7, 6, 3],
    'titanium': [3, 7, 6, 3], 
    'anodized_titanium': [3, 7, 6, 3],
    'iridium': [4, 9, 7, 4],
    'mithril': [4, 8, 6, 3]
}
TOUGHNESS_VALUES = {
    'copper': [1, 1, 1, 1],
    'silver': [1, 1, 1, 1], 
    'soul_steel': [2, 2, 2, 2],
    'titanium': [2, 2, 2, 2], 
    'anodized_titanium': [2, 2, 2, 2],
    'iridium': [3, 3, 3, 3],
    'mithril': [4, 4, 4, 4]
}