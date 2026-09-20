#include <stdio.h>
#include <assert.h>

int main() {
    int i = 200;

    while (i >= 0) {
        if (i % 10 == 0) {
            printf("%d\n", i);
        }
        --i;
        assert(i >= 0);
    }

    printf("Final value: %d\n", i);

    return 0;
}