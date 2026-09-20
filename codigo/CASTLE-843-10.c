#include <stdio.h>

#define GET_FLOAT_BITS_AS_INT(i) i

void printNum(int num) {
    printf("%d\n", num);
}

int main() {
    int a = 55;
    float b = 1.8f;

    printNum(GET_FLOAT_BITS_AS_INT(a));
    printNum(GET_FLOAT_BITS_AS_INT(b));

    return 0;
}