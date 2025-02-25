# in minecraft, you want to craft an item. Unfortunately, you don't know how much stuff you'll need
# Given the item you want to make and several recipes, determine how much of each base material you'll need to make the item.

# Notes:

#     A recipe is a mapping from an item I to a list of item counts. Each item count consists of some item J and an integer n, indicating that you need n of item J to craft item I.
#     A base material is an item that does not have a recipe. Disregard base materials you don't need.

# Since the amounts can be very large, output each amount mod 1,000,000,000.

# pyright: strict

from oj import ItemCount, Recipe

def mats_needed(item: str, recipes: list[Recipe]) -> frozenset[ItemCount]:
    recipe_dict = {recipe.item: recipe.ingredients for recipe in recipes}
    needed = {item: 1}
    base_materials: dict[str, int] = {}

    while needed:
        current_needed = needed.copy()
        needed.clear()

        for current_item, current_count in current_needed.items():
            if current_item in recipe_dict:
                for ingredient in recipe_dict[current_item]:
                    if ingredient.item in needed:
                        needed[ingredient.item] += ingredient.count * current_count
                    else:
                        needed[ingredient.item] = ingredient.count * current_count
            else:
                if current_item in base_materials:
                    base_materials[current_item] += current_count
                else:
                    base_materials[current_item] = current_count

    result = frozenset(ItemCount(item, count % 1_000_000_000) for item, count in base_materials.items())
    return result


# def mats_needed(item: str, recipes: List[Recipe]) -> frozenset[ItemCount]:
#     MOD = 1_000_000_000
    
#     # Build a lookup dictionary for recipes
#     recipe_map: Dict[str, List[ItemCount]] = {recipe.item: recipe.ingredients for recipe in recipes}
    
#     def compute_materials(target: str, quantity: int, memo: Dict[str, Dict[str, int]]) -> Dict[str, int]:
#         if target not in recipe_map:  # Base material
#             return {target: quantity}
        
#         if target in memo:  # Use memoization to avoid recomputation
#             return {k: (v * quantity) % MOD for k, v in memo[target].items()}
        
#         total_materials: defaultdict[str, int] = defaultdict(int)
#         for ingredient in recipe_map[target]:
#             sub_materials = compute_materials(ingredient.item, ingredient.count * quantity, memo)
#             for mat, count in sub_materials.items():
#                 total_materials[mat] = (total_materials[mat] + count) % MOD
        
#         memo[target] = total_materials
#         return total_materials
    
#     # Start calculation
#     materials = compute_materials(item, 1, {})
    
#     # Convert to frozenset[ItemCount]
#     return frozenset(ItemCount(item=mat, count=count) for mat, count in materials.items())

assert mats_needed("bed", [
        Recipe(item="bed", ingredients=[
            ItemCount(item="plank", count=3),
            ItemCount(item="wool", count=3),
        ]),
        Recipe(item="wool", ingredients=[
            ItemCount(item="string", count=4),
        ]),
    ]) == frozenset([
        ItemCount(item="string", count=12),
        ItemCount(item="plank", count=3),
    ])

assert mats_needed("diamond_sword", [
        Recipe(item="diamond_sword", ingredients=[
            ItemCount(item="diamond", count=2),
            ItemCount(item="stick", count=1),
        ]),]) == frozenset([
        ItemCount(item="diamond", count=2),
        ItemCount(item="stick", count=1),
    ])

# edge cases
assert mats_needed("chest", [
        Recipe(item="chest", ingredients=[
            ItemCount(item="plank", count=8),
        ]),
    ]) == frozenset([
        ItemCount(item="plank", count=8),
    ])

assert mats_needed("torch", [
        Recipe(item="torch", ingredients=[
            ItemCount(item="stick", count=1),
            ItemCount(item="coal", count=1),
        ]),
    ]) == frozenset([
        ItemCount(item="stick", count=1),
        ItemCount(item="coal", count=1),
    ])

assert mats_needed("ladder", [
        Recipe(item="ladder", ingredients=[
            ItemCount(item="stick", count=7),
        ]),
    ]) == frozenset([
        ItemCount(item="stick", count=7),
    ])

# the length of each item list is 1
assert mats_needed("diamond_sword", [
        Recipe(item="diamond_sword", ingredients=[
            ItemCount(item="diamond", count=2),
        ]),
    ]) == frozenset([
        ItemCount(item="diamond", count=2),
    ])

assert mats_needed("barrel", [
        Recipe(item="barrel", ingredients=[
            ItemCount(item="plank", count=7),
            ItemCount(item="chest", count=1),
        ]),
        Recipe(item="chest", ingredients=[
            ItemCount(item="plank", count=8),
        ]),
    ]) == frozenset([
        ItemCount(item="plank", count=15),
    ])