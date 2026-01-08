#include <stdio.h>

typedef union {
    int integer;
    float real;
} IntOrReal;

void printNum(int num) {
    printf("%d\n", num);
}

int main() {
    IntOrReal a;
    a.integer = 5;
    printNum(a.integer);

    IntOrReal b;
    b.real = 5.8;
    printNum(b.integer);

    return 0;
}