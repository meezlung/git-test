# in minecraft, you want to craft an item. Unfortunately, you don't know how much stuff you'll need
# Given the item you want to make and several recipes, determine how much of each base material you'll need to make the item.

# Notes:

#     A recipe is a mapping from an item I to a list of item counts. Each item count consists of some item J and an integer n, indicating that you need n of item J to craft item I.
#     A base material is an item that does not have a recipe. Disregard base materials you don't need.

# Since the amounts can be very large, output each amount mod 1,000,000,000.

# pyright: strict

from dataclasses import dataclass

@dataclass(frozen=True)
class ItemCount:
    item: str
    count: int

@dataclass(frozen=True)
class Recipe:
    item: str
    ingredients: list[ItemCount]

def mats_needed(item: str, recipes: list[Recipe]) -> frozenset[ItemCount]:
    recipe_dict = {recipe.item: recipe.ingredients for recipe in recipes}
    needed = {item: 1}
    base_materials: dict[str, int] = {}

    print(recipe_dict)

    while needed:
        print("need", needed)
        current_item, current_count = needed.popitem()

        print("curr", current_item, current_count)
        if current_item in recipe_dict:
            print("current item in recipe_dict")
            for ingredient in recipe_dict[current_item]:
                if ingredient.item in needed:
                    print("ingredient in needed")
                    needed[ingredient.item] += ingredient.count * current_count
                else:
                    print("ingredient not in needed")
                    needed[ingredient.item] = ingredient.count * current_count
        else:
            print("current item not in recipe_dict")
            if current_item in base_materials:
                print("current item in base_materials")
                base_materials[current_item] += current_count
            else:
                print("current item not in base_materials")
                base_materials[current_item] = current_count

        print("new need", needed)
        print("base", base_materials)
        print()


    return frozenset(ItemCount(item, count % 1_000_000_000) for item, count in base_materials.items())


assert mats_needed("bed", [
        Recipe(item="bed", ingredients=[
            ItemCount(item="wool", count=3),
            ItemCount(item="plank", count=3),
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

assert mats_needed("bed", [
        Recipe(item="bed", ingredients=[
            ItemCount(item="wool", count=3),
            ItemCount(item="plank", count=3),
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
            ItemCount(item="chest", count=1),
            ItemCount(item="plank", count=7),
        ]),
        Recipe(item="chest", ingredients=[
            ItemCount(item="plank", count=8),
        ]),
    ]) == frozenset([
        ItemCount(item="plank", count=15),
    ])

assert mats_needed("planks", [
        Recipe(item="planks", ingredients=[
            ItemCount(item="log", count=1),
        ]),
    ]) == frozenset([
        ItemCount(item="log", count=1),
    ])