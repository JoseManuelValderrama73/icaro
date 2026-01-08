#include <stdio.h>

#define ITERS 9000

int main() {
    for (int i = 0; i < ITERS; i++) {
        printf("loop\n");
        i--;
    }
    return 0;
}