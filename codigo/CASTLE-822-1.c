#include <stdio.h>
#include <stdlib.h>

void processData(int *data) {
    printf("Data: %d\n", *data);
}

int main() {
    int *ptr = NULL;
    int input;

    printf("Enter a number: ");
    scanf("%9d", input);

    ptr = (int *)malloc(sizeof(int));
    if (ptr == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }
    ptr = input;

    processData(ptr);

    free(ptr);

    return 0;
}