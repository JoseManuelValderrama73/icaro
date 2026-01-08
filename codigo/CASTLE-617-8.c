#include <stdio.h>
#include <assert.h>

#define true 0
#define false 1

int main() {
    assert(!true);
    assert(false);

    printf("Run Completed\n");

    return 0;
}