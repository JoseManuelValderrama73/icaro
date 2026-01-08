#include <stdio.h>
#include <float.h>

int main() {
    float chipWithoutMagnification = 1.0e-38;
    float chipWithMagnification = chipWithoutMagnification / 1.0e38;

    printf("Without: %e\n", chipWithoutMagnification);
    printf("With: %e\n", chipWithMagnification);

    // Is the resut zero?
    if (chipWithMagnification == 0.0) {
        printf("The result is zero.\n");
    } else {
        printf("The result is %e\n", chipWithMagnification);
    }

    return 0;
}