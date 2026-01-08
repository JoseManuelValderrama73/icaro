#include <stdio.h>

int sumArray(int* arr, int size, int index) {
    if (index == size) {
        index = 0;
    }

    return arr[index] + sumArray(arr, size, index+1);
}

int main() {
    int arr[] = {1, 2, 3, 4, 5};
    int sum = sumArray(arr, 5, 0);
    printf("Sum: %d\n", sum);
    return 0;
}