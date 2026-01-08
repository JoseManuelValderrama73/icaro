#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)
{
    char password[15];
    int grant = 0;
    printf("Enter your password: ");
    fgets(password, sizeof(password), stdin);
    if (strcmp(password, "TopSecret!") == 0) grant=1;
    if (grant)
    {
        printf("Access granted\n");
        printf("Please visit: /dashboards for next instructions\n");
    }
    else
    {
        printf("\nAccess denied\n");
    }
    return 0;
}