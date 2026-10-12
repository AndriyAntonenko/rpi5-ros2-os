SUMMARY = "Custom Raspberry Pi 5 image with SSH"
LICENSE = "MIT"
inherit core-image

IMAGE_FEATURES += "ssh-server-openssh"
IMAGE_INSTALL:append = " \
    kernel-modules \
    wpa-supplicant iw wireless-regdb-static \
    linux-firmware-rpidistro-bcm43455 \
    wifi-config \
    andrii-user \
    boot-config \
    avahi-daemon \
"
