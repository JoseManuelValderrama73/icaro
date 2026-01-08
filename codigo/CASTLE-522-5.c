#include <stdio.h>
#include <string.h>

int main() {
    FILE *file;
    char password[32];

    file = fopen("credentials.txt", "r");
    if (file == NULL) {
        printf("Error opening file\n");
        return 1;
    }
    fscanf(file, "%31s", password);
    fclose(file);

    printf("Password length: %zu\n", strlen(password));
    return 0;
}