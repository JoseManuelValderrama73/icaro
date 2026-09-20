#include <stdio.h>

int main(int argc, char **argv) {
    if (argc > 1) {
        char buffer[1024];
        snprintf(buffer, sizeof(buffer), argv[1]);
        printf("%s", buffer);
    }
    return 0;
}