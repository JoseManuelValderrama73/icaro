#include <stdio.h>

#define ARRAY_LEN 200

int main() {
    int a[ARRAY_LEN];
    for (int i = 0; i < ARRAY_LEN; ++i) {
        a[i] = 3 * i + 2;
    }

    int lastInd = ARRAY_LEN - 1;
    for (int i = lastInd; i >= lastInd - ARRAY_LEN; --i) {
        printf("%d, ", a[i]);
    }
    printf("\n");

    return 0;
}