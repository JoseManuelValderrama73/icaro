#include <stdio.h>
#include <stdlib.h>

int main() {
    int a = 1;
    int b = 0;
    printf("%d\n", 1/(b-a)); // There is a known issue in this line!!
    return 0;
}