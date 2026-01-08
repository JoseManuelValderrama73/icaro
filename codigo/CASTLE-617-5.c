#include <stdio.h>
#include <assert.h>

int main() {
    double d = 3.14;

    do {
        assert(d < 0);
        d += 1.23;
    } while (d < 0);

    printf("Final value: %f\n", d);

    return 0;
}