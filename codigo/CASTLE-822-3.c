#include <stdio.h>
#include <stdlib.h>

int main(const int argc, const char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <number>\n", argv[0]);
        return 1;
    }

    // Convert the command line argument to an integer
    char *endptr;
    long int number = strtol(argv[1], &endptr, 10);

    // Check for conversion errors
    if (*endptr != '\0') {
        fprintf(stderr, "Invalid input: '%s' is not a valid number\n", argv[1]);
        return 1;
    }

    int *ptr = NULL;
    ptr = (int*)malloc(sizeof(int));
    if (ptr == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }
    ptr += number;

    printf("Number: %d\n", *ptr);

    free(ptr);

    return 0;
}