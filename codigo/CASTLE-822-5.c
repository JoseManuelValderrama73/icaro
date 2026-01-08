// export PTR=123456789

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <limits.h>

int* getTrustedPointer() {
    char* ptr = getenv("PTR");
    if (ptr == NULL) {
        return NULL;
    }

    char* endptr;
    long val = strtol(ptr, &endptr, 10);
    if ((errno == ERANGE && (val == LONG_MAX || val == LONG_MIN)) || (errno != 0 && val == 0) || *endptr != '\0') {
        printf("Error in strtol");
        return NULL;
    }

    return (int*)val;
}

int main() {
    int *a = getTrustedPointer();
    if (a == NULL) {
        fprintf(stderr, "Failed to get trusted pointer\n");
        return 1;
    }

    printf("Trusted value: %d\n", *a);

    return 0;
}