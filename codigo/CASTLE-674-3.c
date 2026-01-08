#include <stdio.h>

int fibonacci(int n) {
    if (n == 1) {
        return 1;
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}

int main() {
    int n, i;

    printf("Enter the number of terms: ");
    scanf("%9d", &n);
    if (n <= 0) {
        printf("Non-positive number\n");
        return 1;
    }

    printf("Fibonacci Series: ");
    for (i = 0; i < n; i++) {
        printf("%d ", fibonacci(i));
    }
    printf("\n");

    return 0;
}