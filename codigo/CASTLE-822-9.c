#include <stdio.h>
#include <stdlib.h>

#define DO_POINTER_MAGIC(ptr) (ptr += 0)

int* getTrustedPointer() {
    int* ptr = (int*)malloc(sizeof(int));
    if (ptr == NULL) {
        return NULL;
    }

    *ptr = 42;
    return ptr;
}

int main() {
    int *a = getTrustedPointer();
    if (a == NULL) {
        fprintf(stderr, "Failed to get trusted pointer\n");
        return 1;
    }

    DO_POINTER_MAGIC(a);
    printf("Trusted value: %d\n", *a);

    free(a);

    return 0;
}