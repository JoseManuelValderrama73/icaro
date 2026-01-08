#include <stdio.h>
void countdown(int i) {
    printf("%d...\n", i);

    if (i == 0) {
        return;
    }

    countdown(i--);
}

int main() {
    countdown(5);
    return 0;
}