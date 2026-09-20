#include <stdio.h>
#include <stdlib.h>

int main() {
    int* a = (int*)malloc(sizeof(int) * 10);
    if (a == NULL) {
        printf("Failed to allocate memory.\n");
        return 1; // Indicate error and exit
    }

    for (int i = 0; i < 10; ++i) {
        a[i] = i * 8 - 6;
    }

    int** p = &a;
    for (int i = 0; i < 10; ++i) {
        printf("%d\n", **p);
        if (i < 9) {
            ++(*p);
        }
    }

    free(a);

    return 0;
}