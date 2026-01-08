#include <stdio.h>
#include <stdlib.h>

int main() {
    int n=3;
    printf("Enter 3 number (maximum 3 digits)");
    int *arr = (int*) malloc(n * sizeof(int));
    if (arr == NULL) {
    	printf("Memory allocation failed\n");
    	return -1;
    }
    for(int i = 0; i < n; i++) {
        scanf("%3d", &arr[i]);
    }
    printf("The element of the arraye are: ");
    for(int i = 0; i < n; i++) {
		printf(" %d ", arr[i]);
    }

    free(arr);

    return 0;
}