#include <stdio.h>
#include <stdlib.h>

void dosth() {
    int *A = (int*) malloc(sizeof(int) * 10);
    if (A == NULL) {
        perror("Could not reserve memory!");
        return;
    }

    for (int i = 1; i < 4; i++) {
        A[i] = i;
    }

    printf("%d", A[1]);
}

int main() {
    dosth();
    return 0;
}