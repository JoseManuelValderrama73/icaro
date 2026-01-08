#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    char cat[] = "cat ";
    char *command;
    unsigned long long commandLength;

    if (argc != 2) {
        printf("Usage: %s <file_path>\n", argv[0]);
        return 1;
    }

    commandLength = strlen(cat) + strlen(argv[1]) + 1;
    command = (char*) malloc(commandLength);
    if (command == NULL) {
        return 1;
    }
    
    strncpy(command, cat, commandLength);
    strncat(command, argv[1], (commandLength - strlen(cat)) );

    system(command);
    free(command);
    return 0;
}