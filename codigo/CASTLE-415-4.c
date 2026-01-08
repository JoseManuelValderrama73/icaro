#include <stdio.h>
#include <stdlib.h>

int main() {
    int *a = (int*) malloc(sizeof(int));

    if (a == NULL) {
        printf("Failed to allocate memory.\n");
        return 1; // Indicate error and exit
    }

    free(a);
    free(a);

    return 0;
}