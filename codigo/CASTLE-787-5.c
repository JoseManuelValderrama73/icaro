//FormAI DATASET v1.0 Category: Levenshtein Distance Calculator ; Style: detailed
#include <stdio.h>
#include <string.h>

//Function to calculate minimum of three values
int min(int a, int b, int c) {
    int minimum = a;
    if(b < minimum) {
        minimum = b;
    }
    if(c < minimum) {
        minimum = c;
    }
    return minimum;
}

//Function to calculate the Levenshtein Distance between two strings
int levenshteinDistance(char *str1, char *str2) {
    int len1 = strlen(str1), len2 = strlen(str2);
    //Create a 2D array of dimensions len1+1 and len2+1, initialized with 0
    int dp[len1+1][len2+1];
    memset(dp, 0, sizeof(dp));

    //Initialize first row and column with 0 to len of respective strings
    for(int i = 0; i <= len1; i++) {
        dp[i][0] = i;
    }
    for(int j = 0; j <= len2; j++) {
        dp[0][j] = j;
    }

    
    for(int i = 1; i <= len1; i++) {
        for(int j = 1; j <= len2; j++) {
            if(str1[i-1] == str2[j-1]) {
                dp[i][j] = dp[i-1][j-1];
            } else {
                dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1]);
            }
        }
    }
    //Return the bottom-right element of the array which contains the Levenshtein Distance
    return dp[len1][len2];
}

int main() {
    char str1[20], str2[20];
    printf("Enter first string: ");
    fgets(str1, sizeof(str1), stdin);
    printf("Enter second string: ");
    scanf("%s", str2);
    int distance = levenshteinDistance(str1, str2);
    printf("The Levenshtein Distance between %s and %s is %d", str1, str2, distance);
    return 0;
}