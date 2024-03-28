import os 
import json
from dataclasses import dataclass

abspath = os.path.abspath(__file__)
dir_name = os.path.dirname(abspath)
os.chdir(dir_name)

@dataclass(frozen=True, order=True)
class Material: 
    name: str = 'material' # 'item_name' component
    custom_name: str = 'Custom Material' # 'custon_name' component
    base_damage: int = 0
    
    
@dataclass(frozen=True, order=True)
class WeaponType: 
    name: str = 'weapon'
    custom_name: str = 'Custom Weapon'
    base_damage: int = 0