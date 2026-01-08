#include <stdio.h>

int main(int argc, char **argv) {
    char buffer[256];
    if (fgets(buffer, sizeof(buffer), stdin) == NULL) {
        return 1;
    }

    printf(buffer);
    return 0;
}