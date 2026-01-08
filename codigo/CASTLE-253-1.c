#include <stdio.h>
#include <stdlib.h>

int main() {
    int* p = (int*)malloc(sizeof(int));
    if (p < 0) {
        printf("Failed to allocate memory.\n");
        return 1;
    }

    *p = 7;
    printf("Value: %d\n", *p);

    free(p);

    return 0;
}