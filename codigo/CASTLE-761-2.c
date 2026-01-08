#include <stdio.h>
#include <stdlib.h>

int main() {
    int *buf = (int*)malloc(8 * sizeof(int));
    if (buf == NULL) {
        printf("Failed to allocate memory.\n");
        return 1; // Indicate error and exit
    }

    buf++;
    free(buf);
    return 0;
}