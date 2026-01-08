#include <stdio.h>

int main() {
    int a[200];
    for (int i = 0; i < 200; ++i) {
        a[i] = i * i;
    }

    int arrayLength = sizeof(a) / sizeof(char);
    for (int i = 0; i < arrayLength; ++i) {
        printf("%d, ", a[i]);
    }
    printf("\n");

    return 0;
}