#include <stdio.h>

#define INT_MAX 255

int main() {
    int a[300];
    for (int i = 0; i < 300; ++i) {
        a[i] = 350 - 3 * i;
    }

    for (int i = 0; i < INT_MAX; ++i) {
        printf("%d, ", a[i]);
    }
    printf("\n");

    printf("Special elem: %d\n", a[INT_MAX]);

    return 0;
}