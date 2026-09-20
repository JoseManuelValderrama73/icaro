#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void getRandom(int* a) {
    srand(time(NULL));
    *a = rand();
}

int main() {
    int random;
    getRandom(&random);
    printf("Trusted value: %d\n", random);

    return 0;
}