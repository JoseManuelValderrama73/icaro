#include <stdio.h>
#include <string.h>

void printNum(int num) {
    printf("%d\n", num);
}

int main() {
    int a = 55;
    float b = 1.f;

    printNum(a);
    printNum(b);

    return 0;
}