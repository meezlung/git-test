#include <stdio.h>
#include "cross_count.h"

int64_t count_crosses(int64_t p) {
    int64_t count = 0;
    // We only need to check values of a such that a^2 < p.
    for (int64_t a = 1; a * a < p; ++a) {
        if (p % a == 0) {
            int64_t q = p / a;
            int64_t diff = q - a;
            // diff must be positive and divisible by 4, and diff/4 must be at least 1.
            if (diff >= 4 && diff % 4 == 0) {
                count++;
            }
        }
    }
    return count;
}
