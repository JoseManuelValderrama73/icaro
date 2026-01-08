#include <openssl/des.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

// echo "18812f545d4d12ac" > key.txt

int min(int a, int b) {
    return a < b ? a : b;
}

void des_encrypt(const char* plaintext, char* ciphertext, const unsigned char key[8])
{
    DES_cblock desKey;
    memcpy(desKey, key, 8);
    DES_set_odd_parity(&desKey);

    DES_key_schedule schedule;
    DES_set_key_unchecked(&desKey, &schedule);

    const size_t plaintextLength = strlen(plaintext);
    for (size_t i = 0; i < plaintextLength; i += 8) {
        DES_cblock input;
        memset(input, '0', 8); // '0' for padding
        memcpy(input, plaintext + i, min(8, plaintextLength - i));

        DES_cblock output;
        DES_ecb_encrypt(&input, &output, &schedule, DES_ENCRYPT);

        for (int j = 0; j < 8; j++) {
            sprintf(ciphertext + 2 * i + 2 * j, "%02x", output[j]);
        }
    }
}

int read_key(const char *filename, unsigned char key[8]) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        fprintf(stderr, "Could not open file: %s\n", filename);
        return 0;
    }

    char key_hex[17];

    if (fscanf(file, "%16s", key_hex) != 1) {
        fprintf(stderr, "Invalid format in file: %s\n", filename);
        fclose(file);
        return 0;
    }

    fclose(file);

    for (int i = 0; i < 8; i++) {
        sscanf(key_hex + 2 * i, "%2hhx", &key[i]);
    }

    return 1;
}

int main() {
    char sensitiveText[1024];
    printf("Sensitive text: ");
    fgets(sensitiveText, sizeof(sensitiveText), stdin);
    sensitiveText[strcspn(sensitiveText, "\n")] = '\0';

    unsigned char key[8];
    if (!read_key("key.txt", key)) {
        return 1;
    }

    char ciphertext[2048];
    des_encrypt(sensitiveText, ciphertext, key);

    printf("Encrypted: %s\n", ciphertext);

    memset(key, 0, sizeof(key));
    memset(sensitiveText, 0, sizeof(sensitiveText));

    return 0;
}