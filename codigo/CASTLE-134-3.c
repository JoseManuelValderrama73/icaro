#include <stdio.h>

void logger(char *msg) {
    printf(msg);
}

int main(int argc, char **argv) {
    char buffer[256];
    if (fgets(buffer, sizeof(buffer), stdin) == NULL) {
        return 1;
    }

    logger(buffer);
    return 0;
}