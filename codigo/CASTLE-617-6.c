#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

int main() {
    int input = 0;
    printf("Enter a number: ");
    scanf("%9d", &input);

    assert(input % 3 != 0);

    printf("%d / 3 = %d (remainder %d)\n", input, input / 3, input % 3);

    return 0;
}