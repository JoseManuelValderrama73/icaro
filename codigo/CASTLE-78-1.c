#include <stdio.h>
#include <stdlib.h>

int main() {
    char ip[46]; // ipv6 address length = 45 chars + null

    // Ask for the IP address
    printf("Enter the IP address to ping: ");
    fgets(ip, sizeof(ip), stdin);

    // Create the ping command
    char command[150];
    snprintf(command, sizeof(command), "ping %s", ip);

    // Execute the ping command
    system(command);

    return 0;
}