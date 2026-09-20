#include <stdio.h>
#include <string.h>

#define SRC_STRING "random string that definitely has no issues"

int main()
{
    char dataBuffer[100] = "";
    char * data = dataBuffer;

    if (snprintf(data, 100 - strlen(SRC_STRING) -1, "%s\n", SRC_STRING) == 0)
    {
        printf("snprintf failed!");
    }

    printf("%s\n", data);
    return 0;
}