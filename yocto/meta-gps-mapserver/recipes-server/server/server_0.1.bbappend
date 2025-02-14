RDEPENDS_${PN} += "python3 python3-pip"


do_install:append() {
    bberror "Test if works !"
    #pip3 install flask pyserial requests

    #echo "my_custom_entry:12345:respawn:/path/to/custom/command" >> ${IMAGE_ROOTFS}${sysconfdir}/inittab
    
}

do_rootfs:append() {
    # Install flask via pip
    pip3 install flask pyserial requests
}
