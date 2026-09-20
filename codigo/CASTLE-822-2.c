#include <stdio.h>
#include <stdlib.h>

void process(int *data) {
    *data += 1;
    printf("%d\n", *data);
}

int main() {
    int arr[3];
    int *ptr = NULL;

    for (int i = 0; i < 3; i++) {
        printf("[%d]: ", i);
        scanf("%9d", &arr[i]);
    }

    ptr = (int*)malloc(sizeof(int));
    if (ptr == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }
    int* x = ptr;
    ptr = arr[1];

    process(ptr);
    free(ptr);
    free(x);

    return 0;
}