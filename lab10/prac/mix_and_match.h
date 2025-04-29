#ifndef _MIX_AND_MATCH_H
#define _MIX_AND_MATCH_H

#include <stdint.h>

// need to implement
typedef struct MixAndMatch MixAndMatch;
MixAndMatch *init(int a, int m, int d, int64_t *A, int64_t *M, int64_t *D);
int64_t num_meals(MixAndMatch *m, int64_t t);

#endif
