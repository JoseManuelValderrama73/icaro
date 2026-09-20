#include <stdio.h>

int main() {
    int x=77;
    int y=x*x*x;
    int z=y*y;
    unsigned int r= z/1000;
    printf("Result %u\n", r);
    return 0;
}