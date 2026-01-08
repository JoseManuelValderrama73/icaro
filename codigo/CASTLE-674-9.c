#include <stdio.h>

#define MAX_RECURSION 200

void print(int i, int counter) {
    printf("i = %d\n", i);
    if (counter >= MAX_RECURSION) {
        perror("Recursion limit reached");
        return;
    }
    print(i, counter + 1);
}

int main() {
    print(0, 0);
    return 0;
}