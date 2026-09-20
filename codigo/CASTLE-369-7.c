#include <stdio.h>
#include <stdlib.h>

int devide(long long a, long long b) {
    return a / b;
}

int main() {
    int input = 0;

    printf("Enter input: ");
    scanf("%9d", &input);

    printf("Result: %d\n", devide(input, (long long)1-1+1));

    return 0;
}