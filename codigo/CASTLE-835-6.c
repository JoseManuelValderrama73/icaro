#include <stdio.h>

int func1(int a, int b)
{
    if (a > 0 && b > 0)
    {
        return 1;
    }
    return 0;
}

int main() {
    while (func1(1, 1)) {
        printf("positives\n");
    }
    return 0;
}