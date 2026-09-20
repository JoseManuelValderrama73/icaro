#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[])
{
    char username[10];
    strcpy(username,"Is_this_too_long_for_this_array_buffer?");
    printf("Hello  %s!\n", username);

    return 0;
}