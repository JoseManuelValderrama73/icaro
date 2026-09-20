#include <stdio.h>
#include <string.h>

void printNum(int num) {
    printf("%d\n", num);
}

int main() {
    float a = 1.99f;
    double b = a;
    int c = b;
    float d = c;

    printNum(d);

    return 0;
}