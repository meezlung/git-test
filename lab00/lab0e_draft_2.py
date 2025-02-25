from oj import ItemCount, Recipe

MOD = 1_000_000_000

def mats_needed(item: str, recipes: list[Recipe]) -> frozenset[ItemCount]:
    recipe_map = {recipe.item: recipe.ingredients for recipe in recipes}
    memo: dict[str, dict[str, int]] = {}

    def get_base_materials(item: str, count: int) -> dict[str, int]:
        #if this is a base material (no recipe exists)
        if item not in recipe_map:
            return {item: count}
        
        #if already computed, reuse the memoized result
        if item in memo:
            return {k: (v * count) % MOD for k, v in memo[item].items()}
        
        #calculate required materials by decomposing the recipe
        materials: dict[str, int] = {}
        for ingredient in recipe_map[item]:
            ingredient_materials = get_base_materials(ingredient.item, ingredient.count * count)
            for mat, qty in ingredient_materials.items():
                materials[mat] = (materials.get(mat, 0) + qty) % MOD
        
        #store the result in memo and return scaled by `count`
        memo[item] = materials
        return materials

    #get the base materials for the requested item
    result = get_base_materials(item, 1)

    #convert the result to a frozenset of ItemCount objects
    return frozenset(ItemCount(item=mat, count=qty) for mat, qty in result.items())