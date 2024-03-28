import os 
import json

abspath = os.path.abspath(__file__)
dir_name = os.path.dirname(abspath)
os.chdir(dir_name)

# TODO 
# Add [Polexe], [Battleaxe(labrys)]
# Rework [Rapier], [Lance]

tool_types = ['chakram', 'claymore', 'cutlass', 'dagger', 'halberd', 'katana', 'kunai', 'lance', 
                'longaxe', 'longsword', 'rapier', 'saber', 'scythe', 'sickle', 'spear', 'warhammer']
materials = ['wooden', 'golden', 'stone', 'iron', 'diamond', 'netherite',
             'copper', 'silver', 'soul_steel', 'titanium', 'andonized_titanium', 'iridium', 'mithril']

