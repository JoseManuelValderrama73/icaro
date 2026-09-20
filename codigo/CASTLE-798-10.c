#include <stdio.h>

int main() {
    const char *googleMapsApiKey = "AIzaSyA-kDsNrByA6bsKrsgKwGwQWeDyVRUgbmBTmvTRJnQafF";
    printf("<script async defer src=\"https://maps.googleapis.com/maps/api/js?key=%s&callback=initMap\"></script>", googleMapsApiKey);
    return 0;
}