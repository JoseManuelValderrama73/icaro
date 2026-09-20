#include <stdio.h>
#include <stdlib.h>

int main() {
    int *A = (int*) malloc(sizeof(int) * 10); // Here malloc can return NULL!

    for(int i=1; i<=4; i++) {
        A[i] = i;
        // printf("%d\n", A[i]);
    }
    free(A);

    return 0;
}