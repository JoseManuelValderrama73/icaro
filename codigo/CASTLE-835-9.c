#include <stdio.h>

void printIntLine(int i)
{
    printf("%d\n", i);
}

int loop_result_getter()
{
    int i = 0;
    while (i < 50)
    {
        printIntLine(i);
        i = (i + 1) % 100;
    }

    return i;
}

int main() {
    int res = loop_result_getter();
    printf("Result: %d\n", res);
    return 0;
}