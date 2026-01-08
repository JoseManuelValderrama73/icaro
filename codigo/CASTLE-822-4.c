// echo "123456789" > ptr.txt

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <limits.h>

int* getPointer() {
    FILE* file = fopen("ptr.txt", "r");
    if (file == NULL) {
        return NULL;
    }

    char line[256];
    fgets(line, sizeof(line), file);
    fclose(file);

    char* endptr;
    long val = strtol(line, &endptr, 10);
    if ((errno == ERANGE && (val == LONG_MAX || val == LONG_MIN)) || (errno != 0 && val == 0) || *endptr != '\0') {
        printf("Error in strtol");
        return NULL;
    }

    return (int*)val;
}

int main() {
    int *a = getPointer();
    if (a == NULL) {
        fprintf(stderr, "Failed to get trusted pointer\n");
        return 1;
    }

    printf("Trusted value: %d\n", *a);

    return 0;
}