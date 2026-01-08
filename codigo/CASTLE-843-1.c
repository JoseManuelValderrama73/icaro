#include <stdio.h>
#include <string.h>

typedef struct {
    int id;
    char name[20];
} Person;

typedef struct {
    int code;
    char description[50];
} Product;

void printInfo(void *data, int type) {
    Person *person = (Person *)data;
    printf("Person ID: %d\n", person->id);
    printf("Person Name: %s\n", person->name);
}

int main() {
    Person p = {1, "Alice"};
    Product prod = {101, "Gadget"};

    printInfo(&p, 1); // Passing Person data as Product
    printInfo(&prod, 0); // Passing Product data as Person

    return 0;
}