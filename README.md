# energenie
A web interface to an energenie pimote running on the Pi, allowing web control of mains devices

## Installation

### Install lighttpd on a Raspberry Pi

### Configure the cgi module

`sudo cp 99-energenie-cgi.conf /etc/lighttpd/conf-enabled`

`cd /etc/lighttpd/conf-enabled`

`ln -s ../conf-available/10-cgi.conf`

### Checkout or copy this folder into /var/www

### Restart lighttpd

`sudo /etc/init.d/lighttpd restart`

Access http://localhost/energenie on the pi, or replace localhost with the hostname of the pi to access from other devices

Note that although this project uses GPIO, lighttpd doesn't need to run as root, as it uses GPIO safely through sysfs, rather than unsafely through direct access to /dev/mem

