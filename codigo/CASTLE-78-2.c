#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define CMD_MAX 256

int main(int argc, char** argv) {
    char cmd[CMD_MAX] = "/usr/bin/cat ";
    strncat(cmd, argv[1], CMD_MAX - 14);
    system(cmd);
    return 0;
}