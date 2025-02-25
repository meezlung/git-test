#ifndef _POKEDEX_H
#define _POKEDEX_H

#include <stdint.h>

typedef enum Direction { BEFORE, AFTER } Direction;

// provided by the judge
int64_t oj_rand();

// need to implement
typedef struct Pokedex Pokedex;
Pokedex *pd_make();
void pd_catch(Pokedex *p, const char *name);
const char *pd_beside(Pokedex *p,  Direction direction, const char *name);

#endif