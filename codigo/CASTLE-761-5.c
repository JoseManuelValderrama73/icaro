#include <stdio.h>
#include <stdlib.h>

#define GET_ADDRESS(p) (ulli)(p++)

typedef unsigned long long int ulli;

int main() {
    int* a = (int*)malloc(sizeof(int) * 10);
    if (a == NULL) {
        printf("Failed to allocate memory.\n");
        return 1; // Indicate error and exit
    }

    const ulli address = GET_ADDRESS(a);
    printf("The address is 0x%llx\n", address);

    free(a);

    return 0;
}