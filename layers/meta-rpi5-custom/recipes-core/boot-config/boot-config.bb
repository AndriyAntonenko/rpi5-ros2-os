SUMMARY = "Apply Wi-Fi and SSH config from the FAT boot partition at startup"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://boot-config.sh file://boot-config.service"
S = "${WORKDIR}"

inherit systemd
SYSTEMD_SERVICE:${PN} = "boot-config.service"
SYSTEMD_AUTO_ENABLE = "enable"

do_install() {
    install -D -m 0755 ${WORKDIR}/boot-config.sh ${D}${sbindir}/boot-config.sh
    install -D -m 0644 ${WORKDIR}/boot-config.service ${D}${systemd_system_unitdir}/boot-config.service
}

RDEPENDS:${PN} = "andrii-user"
