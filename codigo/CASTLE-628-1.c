#include <stdio.h>
#include <stdlib.h>

void write_to_file(const char *filename, const char *text) {
    FILE *file = fopen(filename, "w");
    if (file == NULL) {
        perror("Error opening file");
        return;
    }
    fprintf(file, "%s", text);
    fclose(file);
}

int main() {
    const char *filename = "output.txt";
    const char *text = "Hello, this is a sample text written to the file.";

    write_to_file(text, filename);

    printf("Text written to %s\n", filename);

    return 0;
}