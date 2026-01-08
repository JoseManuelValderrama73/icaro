#include <stdio.h>
#include <stdlib.h>

int* generateAlwaysNonNullResult() {
    int* a = (int*) malloc(sizeof(int));
    if (a == NULL) {
        perror("Malloc failure");
        exit(1);
    }
    return a;
}

int main() {
    int* a = generateAlwaysNonNullResult();
    printf("AlwaysNonNullResult: %d\n", *a);
    free(a);
    return 0;
}