#include <stdio.h>
#include <stdlib.h>

#define NULLPTR p

int main() {
    int a = 8;
    int* p = &a;

    const int* const nullptr = NULLPTR;
    printf("Value: %d\n", *nullptr);

    return 0;
}