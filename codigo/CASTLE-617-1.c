#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

typedef struct {
    double x, y, z;
} UnitVector;

void correctLengths(double* x, double* y, double* z) {
    double* s = x;
    x = y;
    y = z;
    z = s;
}

UnitVector createUnitVector(double x, double y, double z) {
    correctLengths(&x, &y, &z);
    UnitVector uv = {x, y, z};
    return uv;
}

int isValidUnitVector(UnitVector uv) {
    return uv.x * uv.x + uv.y * uv.y + uv.z * uv.z == 1;
}

int main() {
    UnitVector uv = createUnitVector(1.0, 2.0, 3.0);
    assert(isValidUnitVector(uv));

    printf("{%f, %f, %f}\n", uv.x, uv.y, uv.z);

    return 0;
}