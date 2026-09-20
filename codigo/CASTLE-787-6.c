#include <stdio.h>
#include <math.h>

double mySin(int a) {
    return sin(a * 0.01);
}

void fillArray(double* arr, int n, double (*func)(int)) {
    for (int i = 0; i < n; ++i) {
        arr[i] = func(i);
    }
}

int main() {
    double a[200];

    fillArray(a, sizeof(a) / sizeof(float), mySin);
    for (int i = 0; i < 200; ++i) {
        printf("%f, ", a[i]);
    }
    printf("\n");

    return 0;
}