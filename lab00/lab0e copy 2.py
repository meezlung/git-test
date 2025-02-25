from oj import ItemCount, Recipe
from collections import defaultdict

MOD = 1_000_000_000

def compute_mats(target: str, quantity: int, memo: dict[str, dict[str, int]], recipe_map: dict[str, list[ItemCount]]) -> dict[str, int]:
    if target not in recipe_map:  #base material
        return {target: quantity}
    
    if target in memo:  #use memoization to avoid recomputation
        return {k: (v * quantity) % MOD for k, v in memo[target].items()}
    
    total_mats: defaultdict[str, int] = defaultdict(int)
    for ingredient in recipe_map[target]:
        sub_mats = compute_mats(ingredient.item, ingredient.count * quantity, memo, recipe_map)
        for mat, count in sub_mats.items():
            total_mats[mat] = (total_mats[mat] + count) % MOD
    
    memo[target] = total_mats
    return total_mats

def mats_needed(item: str, recipes: list[Recipe]) -> frozenset[ItemCount]:
    recipe_map: dict[str, list[ItemCount]] = {recipe.item: recipe.ingredients for recipe in recipes}

    mats = compute_mats(item, 1, {}, recipe_map)
    
    return frozenset(ItemCount(item=mat, count=count) for mat, count in mats.items())


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