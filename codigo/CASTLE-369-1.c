#include <stdio.h>
#include <stdlib.h>

int main()
{
    int hello= (8003+1) % 26;
    printf("Result is %d",hello);
    int b=atoi("-42");
    printf("Result is %d",b);
    int test= 17/ (hello+20+b);
    printf("Result is %d",test);
    return 0;
}