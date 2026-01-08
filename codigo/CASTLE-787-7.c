#include <stdio.h>
#include <stdlib.h>

int main() {
    int *A = (int*) malloc(sizeof(int) * 10);

    if (A == NULL) {
        printf("Failed to allocate memory.\n");
        return 1; // Indicate error and exit
    }

    for (int i = 1; i <= 4; i++) {
        A[i] = i;
        printf("%d\n", A[i]);
    }

    free(A);

    return 0;
}
