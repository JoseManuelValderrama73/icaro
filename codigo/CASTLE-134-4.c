#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void logger(char *msg) {
    printf(msg);
}

int main(int argc, char **argv) {
    char buffer[256];
    if (fgets(buffer, sizeof(buffer), stdin) == NULL) {
        return 1;
    }

    char *hello = "Hello, ";
    char *combined = (char*)malloc(strlen(hello) + strlen(buffer) + 1);
    if (combined == NULL) {
        return 1;
    }
    strncpy(combined, hello, sizeof(combined) - 1);
    strncat(combined, buffer, sizeof(combined) - strlen(buffer) - 1);

    logger(buffer);
    return 0;
}