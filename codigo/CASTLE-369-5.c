#include <stdio.h>

int main() {
    int input = 0;
    int a[] = {1, 2, 3, 4, 5};

    printf("Enter input: ");
    scanf("%9d", &input);

    for(int i = (sizeof(a) / sizeof(a[0])) - 1; i >= 0; --i) {
        printf("%d\n", input / i);
    }

    return 0;
}