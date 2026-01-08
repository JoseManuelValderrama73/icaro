#include <stdio.h>
#include <string.h>

int main() {
    char buffer[8];
    int *intPtr = (int*)buffer;

    // Write an integer into the buffer
    strcpy(buffer, "!");

    printf("Integer value: %d\n", *intPtr);
    return 0;
}