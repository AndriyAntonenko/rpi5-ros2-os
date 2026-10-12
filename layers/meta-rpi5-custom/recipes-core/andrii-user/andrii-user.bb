SUMMARY = "User 'andrii': SSH key auth only (key comes from the boot partition), passwordless sudo"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

S = "${WORKDIR}"

inherit useradd
USERADD_PACKAGES = "${PN}"
USERADD_PARAM:${PN} = "-m -d /home/andrii -s /bin/sh -p '*' andrii"

do_install() {
    install -d -m 0700 ${D}/home/andrii/.ssh
    chown -R andrii:andrii ${D}/home/andrii

    install -d -m 0750 ${D}${sysconfdir}/sudoers.d
    echo "andrii ALL=(ALL) NOPASSWD: ALL" > ${D}${sysconfdir}/sudoers.d/andrii
    chmod 0440 ${D}${sysconfdir}/sudoers.d/andrii
}

FILES:${PN} = "/home/andrii ${sysconfdir}/sudoers.d"
RDEPENDS:${PN} = "sudo"
