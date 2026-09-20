#include <stdio.h>

int main() {
    int nondet[2*10000+3];
    for(int i=0; i<=20000; i++) { nondet[i]=i;};

    for(int i=0; i<=40000; i++) {
        printf("%d\n", nondet[i]);
    }

    return 0;
}