#include <stdio.h>
#include <stdlib.h>
#include <curl/curl.h>

int main(void) {
    CURL *curl;
    CURLcode res;
    struct curl_slist *headers = NULL;

    curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, "https://api.github.com/repos/owner/repo");
        headers = curl_slist_append(headers, "Authorization: token ghp_CP4XHQtdppg5JcZqjVM2qv5fXA640eyuzfyZ");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        // GitHub requires a User-Agent header
        curl_easy_setopt(curl, CURLOPT_USERAGENT, "Mozilla/5.0");


        res = curl_easy_perform(curl);
        if(res != CURLE_OK)
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));

        // Cleanup
        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
    }
    return 0;
}