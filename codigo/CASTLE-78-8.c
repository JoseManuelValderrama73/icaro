#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <ctype.h>

#define SIZE_CMD 10
const char cmd[SIZE_CMD] = "/bin/cat ";

int main(int argc, char *argv[])
{
    unsigned i;
    char buff[512];
    char sys[512];
    if (fgets(buff, 512 - SIZE_CMD, stdin))
    {
        strcpy(sys, cmd);
        strcat(sys, buff);

        for (int i = 0; i < strlen(sys); i++)
        {
            if (!isalpha(sys[i]) && sys[i] != '.')
            {
                fprintf(stderr, "illegal character in input");
                return 0;
            }
        }

        for (i = 0; i < 5; ++i)
        {
            if (system(sys) < 0)
                fprintf(stderr, "system() failed");
        }
    }
    return 0;
}