#include <stdio.h>
#include <stdlib.h>

#define CHECK_NULL(ptr) check(ptr)

void check(void *ptr) {
    free(ptr);
}

int main() {
    int *a = (int*) malloc(sizeof(int));

    if (a == NULL) {
        printf("Failed to allocate memory.\n");
        return 1; // Indicate error and exit
    }

    CHECK_NULL(a);
    free(a);

    return 0;
}