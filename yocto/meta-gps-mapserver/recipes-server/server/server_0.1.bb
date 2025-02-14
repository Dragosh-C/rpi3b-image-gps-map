
DESCRIPTION = "Files for server"
LICENSE = "MIT"


LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://etc/init.d/auto_startup \
           file://etc/inittab \
           file://etc/ssh/sshd_config \
           file://root/flask_server/app.py \
           file://root/flask_server/templates/index.html \
           file://root/gps-daemon.py \
           file://root/install_python_libs.py"

do_install() {
    
    install -d ${D}/gps/etc/init.d
    install -m 0644 ${WORKDIR}/etc/init.d/auto_startup ${D}/gps/etc/init.d
    install -m 0644 ${WORKDIR}/etc/inittab ${D}/gps/

    install -d ${D}/gps/ssh
    install -m 0644 ${WORKDIR}/etc/ssh/sshd_config ${D}/gps/ssh/
    install -d ${D}/gps/myapp/flask_server/templates
    install -m 0755 ${WORKDIR}/root/flask_server/app.py ${D}/gps/myapp/flask_server/
    install -m 0644 ${WORKDIR}/root/flask_server/templates/index.html ${D}/gps/myapp/flask_server/templates/

    install -d ${D}/gps/myapp
    install -m 0755 ${WORKDIR}/root/gps-daemon.py ${D}/gps/myapp/
    install -m 0755 ${WORKDIR}/root/install_python_libs.py ${D}/gps/myapp/

}

FILES:${PN} += "/gps*"

