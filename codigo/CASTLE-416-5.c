#include <stdio.h>
#include <stdlib.h>

void doCalcWithoutFree(int* a) {
    int b = *a * *a;
    printf("Result: %d\n", b);
    free(a);
}

int main() {
    int *a = (int*) malloc(sizeof(int));

    if (a == NULL) {
        printf("Failed to allocate memory.\n");
        return 1; // Indicate error and exit
    }

    int* p = a;
    *a = 5;
    *p = 6;

    doCalcWithoutFree(a);
    doCalcWithoutFree(p);

    return 0;
}