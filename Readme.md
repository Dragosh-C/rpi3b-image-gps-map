** Embedded System Implementation of a gps Web Server on RPi **  
---

### Overview  
This project involved setting up a file system for a Raspberry Pi (RPi) using Buildroot, integrating an overlay directory (`my_overlay`) for custom configurations. The system was configured with DHCP and OpenSSH to enable SSH connections to the RPi. Authentication using the root account and password was enabled through configuration file modifications.  

Python 3 and Flask were installed to support scripts for both a daemon and a web server.

The Linux kernel (version 6.12.6) was manually compiled using the mainline source from [kernel.org](https://kernel.org/) and configured with the `defconfig` default configuration file.  

A startup script (`auto_startup`) was set to run automatically from `inittab` to initiate both the data collection script and the Flask web server at boot.  

---

### **HTTP Server**  
The HTTP server is implemented using Flask and displays a map with GPS coordinates. Below the map, it shows the data collected from the GPS daemon. The map and GPS data are rendered using the HTML and JavaScript files located in `templates/index.html`. The JavaScript script fetches data from the `/utc` and `/gps` endpoints to display the relevant information.  

---

### **GPS Daemon**  
The GPS daemon reads data from the serial interface, processes it, and sends it to the web server via POST requests to the `/gps-data` and `/utc-data` endpoints.  

---
### **Files for qemu**

Files required for qemu to run the RPi image are as follows:

```bash

├── bcm2837-rpi-3-b.dtb
├── launch-rpi.sh  \\ script for runing qemu
├── rootfs.img \\ build this using `buildroot` (use buildroot_config and my_overlay) or `yocto`
└── vmlinuz-kernel \\ manually compile the kernel (kernel_config)
```

---

### **Project Structure**  
The project is structured as follows:  

```
├── etc  
│   ├── init.d  
│   │   └── auto_startup  
│   ├── inittab  
│   └── ssh  
│       └── sshd_config  
└── root  
    ├── flask_server  
    │   ├── app.py  
    │   └── templates  
    │       └── index.html  
    ├── gps-daemon.py  
    └── install_python_libs.py  
```  

- **`auto_startup`**: A script to automatically start the data collection and web server.  
- **`inittab`**: Configures the automatic execution of the `auto_startup` script at boot.  
- **`sshd_config`**: SSH configuration file to allow root login and password authentication.  
- **`app.py`**: Flask application file for the web server.  
- **`index.html`**: HTML and JavaScript code for the web interface, displaying the GPS data and map.  
- **`gps-daemon.py`**: The daemon script for collecting and transmitting GPS data.  
- **`install_python_libs.py`**: A script to install required Python libraries (`requests` and `pyserial`).  

---

### **Accessing the Web Server**  
The web server can be accessed at:  
- **URL:** `http://localhost:8888`  

---

### **Connecting to the Raspberry Pi**  
To connect to the RPi via SSH, use the following command:  
```bash  
ssh -p 5555 root@127.0.0.1  
```  
