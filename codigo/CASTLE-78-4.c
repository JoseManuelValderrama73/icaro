#include <stdio.h>
#include <stdlib.h>

int main() {
    char command[256];
    char userInput[10];

    printf("Enter the number of files to list: ");
    fgets(userInput, sizeof(userInput), stdin);

    snprintf(command, sizeof(command), "ls -l | head -n %s", userInput);
    system(command);

    return 0;
}