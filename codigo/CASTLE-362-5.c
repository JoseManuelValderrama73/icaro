#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>


void* write_to_file(void* arg) {
    FILE* file = fopen("logs.txt", "a");
    if (file == NULL) {
        perror("Failed to open file");
        return NULL;
    }

    for (int i = 0; i < 100; i++) {
        fprintf(file, "Thread %ld writing...\n", (long)pthread_self());
        usleep(10);
    }

    fclose(file);
    return NULL;
}

int main() {
    pthread_t thread1, thread2;

    pthread_create(&thread1, NULL, write_to_file, NULL);
    pthread_create(&thread2, NULL, write_to_file, NULL);

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    printf("Logging complete.\n");
    return 0;
}