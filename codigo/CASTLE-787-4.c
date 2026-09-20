#include <stdio.h>
#include <string.h>

int main( int argc, char *argv[])
{
    char string_1[10];
    char string_2[10];
    char string_3[10];

    printf("Enter the first string:");
    fgets(string_1, sizeof(string_1), stdin);
    printf("Your first string is: %s.\n",string_1);
    printf("Enter the second string:");
    fscanf(stdin, "%s", string_2);
    printf("Your second string is: %s.\n",string_2);
    printf("Enter the third string:");
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
    fgets(string_3, sizeof(string_3), stdin);
    printf("Your third string is: %s.\n",string_3);

    return 0;
}