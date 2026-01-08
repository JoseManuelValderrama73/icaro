#include <stdio.h>
#include <math.h>


int main() {
    int a = 101;
    int b = a*a*a;
    int c = b*2+15000;
    int d = c^15;
    int e = d;

    for (int i = 0; i < 3; i++) {
        e *= e;
    }

    printf("%d\n", e);

    return 0;
}