#include "pokedex.h"

#include <assert.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>

void init_oj_rand() {
    // initialize RNG
    // feel free to modify
    srand(time(NULL));
}

int64_t oj_rand() {
    // return a random number
    // feel free to modify
    return rand();
}

void yield_pokemon(const char *name) {
    if (name != NULL) {
        printf("Pokemon found: %s\n", name);
    } else {
        printf("No pokemon found.\n");
    }
}

int main() {
    init_oj_rand();

    Pokedex *pd = pd_make();

    pd_catch(pd, "Pikachu");
    yield_pokemon(pd_beside(pd, BEFORE, "Pikachu"));
    pd_catch(pd, "Bulbasaur");
    yield_pokemon(pd_beside(pd, BEFORE, "Pikachu"));
    yield_pokemon(pd_beside(pd, AFTER, "Pikachu"));
    yield_pokemon(pd_beside(pd, BEFORE, "Magikarp"));
    yield_pokemon(pd_beside(pd, AFTER, "Magikarp"));
    pd_catch(pd, "Magikarp");
    yield_pokemon(pd_beside(pd, BEFORE, "Pikachu"));

    printf("\n");

    // TODO add more tests here


    printf("DONE\n");
}
