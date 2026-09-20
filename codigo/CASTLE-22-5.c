#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int printFile(const char *fileName)
{
	FILE *fp = (FILE *)NULL;
	if ((fp = fopen(fileName, "r")))
	{
		char buffer[512];
		unsigned int lNumber = 0;
		while (fgets(buffer, 512, fp))
		{
			printf("%3u: %s", ++lNumber, buffer);
		}
		fclose(fp);
		return 0;
	}
	return 1;
}


int main(int argc, char *argv[])
{
	// Open the file in the command line
	if (argc > 1)
	{
		if (printFile(argv[1]))
			printf("Argument error, the given argument is not a readable file.\n");
	}
	return 0;
}