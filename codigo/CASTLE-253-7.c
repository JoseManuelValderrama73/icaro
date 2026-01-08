#include <stdio.h>
#include <stdlib.h>

#define IsNegative(x) x == NULL

int main() {
    int* p = (int*)malloc(sizeof(int));
    if (IsNegative(p)) {
        printf("Failed to allocate memory.\n");
        return 1;
    }

    *p = 7;
    printf("Value: %d\n", *p);

    free(p);

    return 0;
}