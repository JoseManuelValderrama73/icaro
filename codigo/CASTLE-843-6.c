#include <stdio.h>

#define CHECK_AND_RETURN(i) (*(int*)&i)

void printNum(int num) {
    printf("%d\n", num);
}

int main() {
    int a = 55;
    float b = 1.f;

    printNum(CHECK_AND_RETURN(a));
    printNum(CHECK_AND_RETURN(b));

    return 0;
}