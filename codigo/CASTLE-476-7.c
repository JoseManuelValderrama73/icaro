#include <stdio.h>
#include <stdlib.h>


int main() {
    int *A = (int*) malloc(sizeof(int) * 10);
    if (A == NULL) {
        return 0;
    }

    for(int i=1; i<=4; i++) {
        A[i] = i;
    }
    free(A);

    return 0;
}