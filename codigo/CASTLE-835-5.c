#include <stdio.h>

void printIntLine(int i)
{
    printf("%d\n", i);
}

int loop_result_getter()
{
    int i = 0;
    while (i >= 0)
    {
        printIntLine(i);
        i = (i + 1) % 256;
    }

    return i;
}

int main() {
    int res = loop_result_getter();
    printf("Result: %d\n", res);
    return 0;
}