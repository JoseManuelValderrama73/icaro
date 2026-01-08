#include <stdio.h>

int fibonacci(int n) {
    if (n < 0) {
        return -1;
    }
    if (n == 0 || n == 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int sqr(int n) {
    return n * n;
}

int main() {
    const int a = 123;
    const int b = 12;

    printf("%d\n", a / (fibonacci(b) - sqr(b)));

    return 0;
}