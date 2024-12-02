import os 
import json
import math
from dataclasses import dataclass, field
from typing import Optional, Union, Dict

from _item_maker import *

abspath = os.path.abspath(__file__)
dir_name = os.path.dirname(abspath)
os.chdir(dir_name)

ITEMS = [
    ItemData("alexandrite", "emerald"),
    ItemData("bacon", "cooked_porkchop", [FoodComponent(8.0, 3, 1.2)])
]

# Main
def main():
    # Run 
    populate_files(ITEMS)
    
    
        
# Main
if __name__ == "__main__":
    main()