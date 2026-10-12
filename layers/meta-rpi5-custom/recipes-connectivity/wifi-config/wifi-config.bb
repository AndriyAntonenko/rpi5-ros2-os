SUMMARY = "Network config: DHCP on Ethernet and Wi-Fi (Wi-Fi credentials come from the boot partition)"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://25-wlan0.network file://20-wired.network file://10-require-config.conf"
S = "${WORKDIR}"

do_install() {
    install -d ${D}${sysconfdir}/systemd/network
    install -m 0644 ${WORKDIR}/25-wlan0.network ${D}${sysconfdir}/systemd/network/
    install -m 0644 ${WORKDIR}/20-wired.network ${D}${sysconfdir}/systemd/network/

    # enable wpa_supplicant@wlan0, but only start it when a config exists
    install -d ${D}${sysconfdir}/systemd/system/multi-user.target.wants
    ln -sf ${systemd_system_unitdir}/wpa_supplicant@.service \
        ${D}${sysconfdir}/systemd/system/multi-user.target.wants/wpa_supplicant@wlan0.service
    install -D -m 0644 ${WORKDIR}/10-require-config.conf \
        ${D}${sysconfdir}/systemd/system/wpa_supplicant@wlan0.service.d/10-require-config.conf
}

FILES:${PN} = "${sysconfdir}"
RDEPENDS:${PN} = "wpa-supplicant"
