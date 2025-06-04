import json
import os
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

@dataclass
class ToolMaterial:
    name_pre: str
    custom_name_pre: str
    attack_damage: float
    item_override_pre: str
    max_durability: Optional[int] = None

@dataclass
class ToolType:
    tool_name: str
    full_name: str
    base_damage: float
    base_speed: float
    item_override_name: str
    bonus_range: Optional[float] = None

class ItemBuilderGenerator:
    def __init__(self):
        # Define tool materials based on your enum
        self.materials = {
            # Minecraft materials
            "wooden": ToolMaterial("wooden", "Wooden", 1.0, "wooden"),
            "golden": ToolMaterial("golden", "Golden", 1.5, "golden"),
            "stone": ToolMaterial("stone", "Stone", 2.0, "stone"),
            "iron": ToolMaterial("iron", "Iron", 3.0, "iron"),
            "diamond": ToolMaterial("diamond", "Diamond", 4.0, "diamond"),
            "netherite": ToolMaterial("netherite", "Netherite", 5.0, "netherite"),
            
            # Odyssey materials
            "copper": ToolMaterial("copper", "Copper", 2.5, "golden", 198),
            "silver": ToolMaterial("silver", "Silver", 3.0, "iron", 337),
            "soul_steel": ToolMaterial("soul_steel", "Soul Steel", 4.0, "iron", 666),
            "titanium": ToolMaterial("titanium", "Titanium", 4.0, "iron", 1002),
            "anodized_titanium": ToolMaterial("anodized_titanium", "Anodized Titanium", 4.0, "iron", 1002),
            "iridium": ToolMaterial("iridium", "Iridium", 5.0, "diamond", 3108),
            "mithril": ToolMaterial("mithril", "Mithril", 6.0, "diamond", 1789),
            "crystal_alloy": ToolMaterial("crystal_alloy", "Crystal Alloy", 4.0, "iron", 1123),
        }
        
        # Define tool types based on your enum
        self.tool_types = {
            # Vanilla tools
            "sword": ToolType("sword", "Sword", 3.0, 1.6, "sword"),
            "pickaxe": ToolType("pickaxe", "Pickaxe", 1.0, 1.2, "pickaxe"),
            "axe": ToolType("axe", "Axe", 5.0, 1.0, "axe"),
            "shovel": ToolType("shovel", "Shovel", 1.5, 1.0, "shovel"),
            "hoe": ToolType("hoe", "Hoe", 0.0, 1.6, "hoe"),
            
            # Sword variants
            "katana": ToolType("katana", "Katana", 3.0, 1.7, "sword", 0.2),
            "claymore": ToolType("claymore", "Claymore", 6.0, 0.9, "sword", 0.5),
            "dagger": ToolType("dagger", "Dagger", 1.0, 3.0, "sword", -0.2),
            "rapier": ToolType("rapier", "Rapier", 1.5, 3.5, "sword"),
            "cutlass": ToolType("cutlass", "Cutlass", 2.5, 2.1, "sword"),
            "saber": ToolType("saber", "Saber", 3.0, 1.8, "sword"),
            "sickle": ToolType("sickle", "Sickle", 1.5, 2.7, "sword", -0.2),
            "chakram": ToolType("chakram", "Chakram", 1.5, 2.5, "sword", -0.3),
            "kunai": ToolType("kunai", "Kunai", 1.0, 2.5, "sword"),
            "longsword": ToolType("longsword", "Longsword", 4.0, 1.5, "sword", 0.3),
            "zweihander": ToolType("zweihander", "Zweihander", 7.0, 0.7, "sword", 0.8),
            "kriegsmesser": ToolType("kriegsmesser", "Kriegsmesser", 6.0, 0.8, "sword", 0.6),
            
            # Shovel variants (polearms)
            "spear": ToolType("spear", "Spear", 3.0, 1.2, "shovel", 2.0),
            "halberd": ToolType("halberd", "Halberd", 5.0, 0.9, "shovel", 3.0),
            "lance": ToolType("lance", "Lance", 3.0, 0.8, "shovel", 3.0),
            
            # Axe variants
            "longaxe": ToolType("longaxe", "Longaxe", 6.0, 0.8, "axe", 0.5),
            "poleaxe": ToolType("poleaxe", "Poleaxe", 4.0, 1.1, "axe", 1.0),
            "glaive": ToolType("glaive", "Glaive", 4.0, 1.3, "axe", 1.0),
            
            # Pickaxe variants
            "warhammer": ToolType("warhammer", "Warhammer", 4.0, 1.4, "pickaxe"),
            
            # Hoe variants
            "scythe": ToolType("scythe", "Scythe", 3.0, 1.1, "hoe", 1.0),
            
            # Special
            "shuriken": ToolType("shuriken", "Shuriken", 0.5, 1.0, "iron_nugget"),
        }

    def calculate_final_damage(self, material: ToolMaterial, tool: ToolType) -> float:
        """Calculate final attack damage: material damage + tool base damage"""
        return material.attack_damage + tool.base_damage

    def calculate_entity_range(self, tool: ToolType) -> float:
        """Calculate entity interaction range modifier"""
        return tool.bonus_range if tool.bonus_range is not None else 0.0

    def generate_item_json(self, material_key: str, tool_key: str) -> List[Dict[str, Any]]:
        """Generate item builder JSON for a specific material-tool combination."""
        
        material = self.materials[material_key]
        tool = self.tool_types[tool_key]
        
        # Calculate final stats
        final_damage = self.calculate_final_damage(material, tool)
        final_speed = tool.base_speed
        entity_range = self.calculate_entity_range(tool)
        
        # Create item identifiers
        item_name = f"{material.name_pre}_{tool.tool_name}"
        display_name = f"{material.custom_name_pre} {tool.full_name}"
        
        # Generate the JSON structure
        item_json = [
            {
                "function": "set_components",
                "components": {
                    "minecraft:item_model": f"odyssey:{item_name}",
                    "minecraft:item_name": item_name
                }
            },
            {
                "function": "minecraft:set_name",
                "entity": "this",
                "name": {
                    "text": display_name,
                    "bold": False,
                    "italic": False
                }
            },
            {
                "function": "minecraft:set_attributes",
                "modifiers": [
                    {
                        "id": "odyssey:item.base_attack_damage",
                        "attribute": "minecraft:attack_damage",
                        "amount": final_damage,
                        "slot": "mainhand",
                        "operation": "add_value"
                    },
                    {
                        "id": "odyssey:item.reset_attack_speed",
                        "attribute": "minecraft:attack_speed",
                        "amount": -4.0,
                        "slot": "mainhand",
                        "operation": "add_value"
                    },
                    {
                        "id": "odyssey:item.base_attack_speed",
                        "attribute": "minecraft:attack_speed",
                        "amount": final_speed,
                        "slot": "mainhand",
                        "operation": "add_value"
                    },
                    {
                        "id": "odyssey:item.base_entity_range",
                        "attribute": "minecraft:entity_interaction_range",
                        "amount": entity_range,
                        "slot": "mainhand",
                        "operation": "add_value"
                    }
                ],
                "replace": True
            }
        ]

        # Extra Components 
        if material.max_durability:
            item_json[0]["components"]["minecraft:max_damage"] = material.max_durability
        
        return item_json

    def generate_all_combinations(self, output_dir: str = "weapons") -> None:
        """Generate all material-tool combinations and save to files."""
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        generated_count = 0
        
        # Generate combinations
        for material_key in self.materials:
            for tool_key in self.tool_types:
                item_json = self.generate_item_json(material_key, tool_key)
                
                # Create filename
                filename = f"{material_key}_{tool_key}.json"
                sub_dir = f"{output_dir}/{tool_key}"
                filepath = os.path.join(sub_dir, filename)
                
                # Write to file
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(item_json, f, indent=2, ensure_ascii=False)
                
                generated_count += 1
                print(f"Generated: {filename}")
        
        print(f"\nTotal files generated: {generated_count}")

    def generate_filtered_combinations(self, material_filter: List[str] = None, 
                                     tool_filter: List[str] = None, 
                                     output_dir: str = "filtered_items") -> None:
        """Generate specific combinations based on filters."""
        
        materials_to_use = material_filter if material_filter else list(self.materials.keys())
        tools_to_use = tool_filter if tool_filter else list(self.tool_types.keys())
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        generated_count = 0
        
        for material_key in materials_to_use:
            if material_key not in self.materials:
                print(f"Warning: Material '{material_key}' not found, skipping...")
                continue
                
            for tool_key in tools_to_use:
                if tool_key not in self.tool_types:
                    print(f"Warning: Tool '{tool_key}' not found, skipping...")
                    continue
                    
                item_json = self.generate_item_json(material_key, tool_key)
                
                filename = f"{material_key}_{tool_key}.json"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(item_json, f, indent=2, ensure_ascii=False)
                
                generated_count += 1
                print(f"Generated: {filename}")
        
        print(f"\nFiltered generation complete: {generated_count} files")

    def generate_summary(self) -> None:
        """Print a summary of all combinations that will be generated."""
        print("=== ITEM COMBINATION SUMMARY ===")
        print(f"Materials: {len(self.materials)}")
        print("Available materials:", ", ".join(self.materials.keys()))
        print(f"\nTool Types: {len(self.tool_types)}")
        print("Available tools:", ", ".join(self.tool_types.keys()))
        print(f"\nTotal Possible Combinations: {len(self.materials) * len(self.tool_types)}")
               
        print("\n=== SAMPLE COMBINATIONS ===")
        sample_materials = ["iron", "diamond", "mithril"]
        sample_tools = ["sword", "dagger", "katana", "warhammer"]
        
        for material_key in sample_materials:
            if material_key in self.materials:
                for tool_key in sample_tools:
                    if tool_key in self.tool_types:
                        material = self.materials[material_key]
                        tool = self.tool_types[tool_key]
                        final_damage = self.calculate_final_damage(material, tool)
                        entity_range = self.calculate_entity_range(tool)
                        
                        range_text = f", range: {entity_range:+.1f}" if entity_range != 0 else ""
                        print(f"{material.custom_name_pre} {tool.full_name}: "
                              f"{final_damage} damage, {tool.base_speed} speed{range_text}")

    def add_material(self, key: str, material: ToolMaterial) -> None:
        """Add a new material to the generator."""
        self.materials[key] = material
        print(f"Added material: {material.custom_name_pre}")

    def add_tool_type(self, key: str, tool: ToolType) -> None:
        """Add a new tool type to the generator."""
        self.tool_types[key] = tool
        print(f"Added tool type: {tool.full_name}")

    def get_material_categories(self) -> Dict[str, List[str]]:
        """Group materials by their origin/category."""
        categories = {
            "minecraft": ["wooden", "golden", "stone", "iron", "diamond", "netherite"],
            "overworld": ["copper", "silver", "titanium", "anodized_titanium", "iridium"],
            "nether": ["soul_steel"],
            "edge": ["mithril", "crystal_alloy"]
        }
        return categories

    def get_tool_categories(self) -> Dict[str, List[str]]:
        """Group tools by their base type."""
        categories = {
            "vanilla": ["sword", "pickaxe", "axe", "shovel", "hoe"],
            "sword_variants": ["katana", "claymore", "dagger", "rapier", "cutlass", "saber", 
                              "sickle", "chakram", "kunai", "longsword", "zweihander", "kriegsmesser"],
            "polearms": ["spear", "halberd", "lance"],
            "axe_variants": ["longaxe", "poleaxe", "glaive"],
            "hammer_variants": ["warhammer"],
            "scythe_variants": ["scythe"],
            "special": ["shuriken"]
        }
        return categories

# Usage examples and main execution
if __name__ == "__main__":
    generator = ItemBuilderGenerator()
    
    # Show what will be generated
    generator.generate_summary()
    
    # Example 1: Generate all combinations
    print("\n" + "="*50)
    print("OPTION 1: Generate ALL combinations")
    print("="*50)
    choice = input("Generate all combinations? (y/n): ").lower().strip()
    
    if choice == 'y':
        print("\nGenerating all combinations...")
        generator.generate_all_combinations(output_dir="weapons")
    
    # Example 2: Generate filtered combinations
    print("\n" + "="*50)
    print("OPTION 2: Generate filtered combinations")
    print("="*50)
    
    # Show categories for easier selection
    print("\nMaterial categories:")
    for category, materials in generator.get_material_categories().items():
        print(f"  {category}: {', '.join(materials)}")
    
    print("\nTool categories:")
    for category, tools in generator.get_tool_categories().items():
        print(f"  {category}: {', '.join(tools)}")
    
    filter_choice = input("\nGenerate filtered combinations? (y/n): ").lower().strip()
    
    if filter_choice == 'y':
        # Example: Generate only high-tier materials with sword variants
        high_tier_materials = ["diamond", "netherite", "mithril", "iridium"]
        sword_variants = ["sword", "katana", "dagger", "longsword", "rapier"]
        
        print(f"\nGenerating combinations for materials: {', '.join(high_tier_materials)}")
        print(f"And tools: {', '.join(sword_variants)}")
        
        generator.generate_filtered_combinations(
            material_filter=high_tier_materials,
            tool_filter=sword_variants,
            output_dir="high_tier_swords"
        )
    
    # Example 3: Add custom items
    print("\n" + "="*50)
    print("OPTION 3: Add custom materials/tools")
    print("="*50)
    
    custom_choice = input("Add custom items? (y/n): ").lower().strip()
    
    if custom_choice == 'y':
        # Add a custom material
        adamantite = ToolMaterial(
            name_pre="adamantite",
            custom_name_pre="Adamantite",
            attack_damage=6.5,
            item_override_pre="netherite",
            max_durability=4000
        )
        generator.add_material("adamantite", adamantite)
        
        # Add a custom tool
        war_scythe = ToolType(
            tool_name="war_scythe",
            full_name="War Scythe",
            base_damage=4.5,
            base_speed=1.2,
            item_override_name="hoe",
            bonus_range=1.5
        )
        generator.add_tool_type("war_scythe", war_scythe)
        
        # Generate just the new combinations
        print("\nGenerating custom combinations...")
        generator.generate_filtered_combinations(
            material_filter=["adamantite"],
            tool_filter=["war_scythe"],
            output_dir="custom_items"
        )
    
    print(f"\nScript completed successfully!")