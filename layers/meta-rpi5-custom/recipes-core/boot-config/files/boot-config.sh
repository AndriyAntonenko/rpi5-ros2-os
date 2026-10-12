#!/bin/sh
# Apply user-provided configuration from the FAT boot partition.
# CRLF line endings are stripped in case the files were edited on Windows.
BOOT=/boot

if [ -f "$BOOT/wpa_supplicant.conf" ]; then
    mkdir -p /etc/wpa_supplicant
    tr -d '\r' < "$BOOT/wpa_supplicant.conf" > /etc/wpa_supplicant/wpa_supplicant-wlan0.conf
    chmod 0600 /etc/wpa_supplicant/wpa_supplicant-wlan0.conf
    echo "boot-config: applied Wi-Fi config"
fi

if [ -f "$BOOT/authorized_keys" ]; then
    mkdir -p /home/andrii/.ssh
    tr -d '\r' < "$BOOT/authorized_keys" > /home/andrii/.ssh/authorized_keys
    chown -R andrii:andrii /home/andrii/.ssh
    chmod 0700 /home/andrii/.ssh
    chmod 0600 /home/andrii/.ssh/authorized_keys
    echo "boot-config: applied SSH authorized_keys"
fi
