#include <stdio.h>
#include <stdlib.h>

void square(int* a) {
    int b = *a;
    *a = b * b;
}

void negate(int* a) {
    *a = -(*a);
    free(a);
}

int main() {
    int *a = (int*) malloc(sizeof(int));

    if (a == NULL) {
        printf("Failed to allocate memory.\n");
        return 1; // Indicate error and exit
    }

    *a = 5;
    square(a);
    printf("Result: %d\n", *a);

    int* p = NULL;
    if (*a > 20) {
        p = a;
    }

    negate(p);
    printf("Result: %d\n", *p);

    return 0;
}