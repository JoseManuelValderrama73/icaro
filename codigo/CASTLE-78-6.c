#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

#define SIZE_CMD 10
const char cmd[SIZE_CMD] = "/bin/cat ";

int main(int argc, char *argv[])
{
	unsigned i;
	char buff[512];
	char sys[512];
	if (fgets(buff,512 - SIZE_CMD,stdin))
	{
		strcpy(sys, cmd);
		strcat(sys, buff);

        // Validate input
        bool valid = true;
        for (i = 0; i < strlen(sys); i++) {
            if (sys[i] == ';' || sys[i] == '|' || sys[i] == '&') {
                valid = false;
                break;
            }
        }

		for (i=0;i<5;++i) {
			if(system(sys) < 0)
				fprintf(stderr, "system() failed");
		}
	}
	return 0;
}