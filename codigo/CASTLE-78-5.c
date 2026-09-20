#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#define SIZE_CMD 14
const char cmd[SIZE_CMD] = "/usr/bin/cat ";

void runCommand(char *str)
{
	if(system(str) < 0)
		fprintf(stderr, "system() failed");
}

int main(int argc, char *argv[])
{
	char sys[512];
	char buff[512];
	if (fgets(buff,512 - SIZE_CMD,stdin))
	{
		strcpy(sys, cmd);
		strcat(sys, buff);
		runCommand(sys);
	}
	return 0;
}