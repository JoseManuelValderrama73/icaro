#include <stdio.h>
#include <assert.h>

int main() {
    double d = 3.14;

    while (d < 0) {
        assert(d < 0);
        d += 1.23;
    }

    printf("Final value: %f\n", d);

    return 0;
}