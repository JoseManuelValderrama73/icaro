#include <stdio.h>
#include <stdlib.h>

int* getIntPtr() {
    return malloc(sizeof(int));
}

int checkIntPtr(int* p) {
    return (long long)p % 2 == 1;
}

int main() {
    int* p = getIntPtr();
    if (checkIntPtr(p)) {
        printf("Failed to allocate memory.\n");
        return 1;
    }

    *p = 7;
    printf("Value: %d\n", *p);

    free(p);

    return 0;
}