#include <stdio.h>
#include <stdlib.h>

void echo()
{
    char dataBuffer[100] = "";
    char * data = dataBuffer;
    printf("Please enter a string: ");

    if (fgets(data, 100, stdin) == NULL)
    {
        printf("fgets failed!\n");
        exit(1);
    }
    printf("%s\n", data);
}

int main()
{
    echo();
    return 0;
}