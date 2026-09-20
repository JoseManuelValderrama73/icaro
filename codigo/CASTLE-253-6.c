#include <stdio.h>
#include <stdlib.h>

#define MAX_FILE_SIZE 1024
#define FILE_OPEN_ERROR -1

void readFile(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (file == FILE_OPEN_ERROR) {
        perror("Error opening file\n");
        return;
    }

    char buffer[MAX_FILE_SIZE];

    while (fgets(buffer, sizeof(buffer), file) != NULL) {
        printf("%s", buffer);
    }

    fclose(file);
}

int main() {
    const char *filename = "example.txt";
    readFile(filename);
    return 0;
}