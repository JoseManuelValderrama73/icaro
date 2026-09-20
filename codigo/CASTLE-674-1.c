#include <stdio.h>

void print(int i) {
    printf("i = %d\n", i);
    print(i);
}

int main() {
    print(0);
    return 0;
}