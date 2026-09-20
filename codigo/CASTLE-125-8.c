#include <stdio.h>

#define MY_SECRET_CHAR 442

int main() {
    char str[] = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                 "sed do eiusmod tempor incididunt ut labore et dolore magna "
                 "aliqua. Ut enim ad minim veniam, quis nostrud exercitation "
                 "ullamco laboris nisi ut aliquip ex ea commodo consequat. "
                 "Duis aute irure dolor in reprehenderit in voluptate velit "
                 "esse cillum dolore eu fugiat nulla pariatur. Excepteur sint "
                 "occaecat cupidatat non proident, sunt in culpa qui officia "
                 "deserunt mollit anim id est laborum.";

    printf("My secret is hidden in: \"%s\"\n", str);
    printf("My secret is: \'%c\'\n", str[MY_SECRET_CHAR]);

    return 0;
}