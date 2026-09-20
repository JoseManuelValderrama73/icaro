#include <stdio.h>

int main() {
    long long int nondet[2*100000+3];
    for(long long int i=0; i<=200000; i++) { nondet[i]=i;};

    for(long long int i=0; i<=40000000; i++) {
        printf("%lld\n", nondet[i]);
    }

    return 0;
}