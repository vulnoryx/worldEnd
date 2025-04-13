#!/bin/bash

# Check if Wi-Fi interface is up
if iwconfig wlan0 &>/dev/null; then
    if [ "$(iwconfig wlan0 | grep -o 'off/any')" == "" ]; then
        # Get SSID and signal level
        ssid=$(iwconfig wlan0 | grep -o 'ESSID:"[^"]*' | cut -d'"' -f2)
        signal=$(iwconfig wlan0 | grep 'Signal level=' | awk '{print $4}' | sed 's/Signal level=//')

        # Display the Wi-Fi information
        # echo "  $ssid $signal dBm"
        echo "%{F#a1c3a2} "
    else
        echo "%{F#a1c3a2} "
    fi
else
    # Display no Wi-Fi connection
    # echo "  Not connected"
    echo "%{F#a1c3a2} "
fi