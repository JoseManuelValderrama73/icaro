#include <stdio.h>
#include <stdlib.h>

struct test {
    double a;
    char symbol;
    char pointer;
    char null;
};

int main() {
    struct test *p = malloc(sizeof(struct test));
    if (p == NULL) {
        printf("Memory allocation failed.\n");
        return 1; // Return a non-zero value to indicate failure
    }

    p->a = 0;
    free(p);

    return 0;
}
