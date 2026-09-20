#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int contains_char(char c, const char *target){
    char *str;
    str = (char*)malloc((strlen(target) + 1) * sizeof(char));
    if (str == NULL) {
        printf("Failed to allocate memory.\n");
        exit(1);
    }

    char *str_copy = str;
    strcpy(str_copy, target);
    while (*str_copy != 0) {
        if( *str_copy == c ){
            free(str);
            return 1;
        }

        str_copy = str_copy + 1;
    }

    free(str);
    return 0;
}

int main() {
    char search = 'a';
    char *text = "banana";

    if (contains_char(search, text)) {
        printf("'%s' contains '%c' character.\n", text, search);
    }
    else {
        printf("'%s' does not contain '%c' character.\n", text, search);
    }
    return 0;
}