# pink-frame
Raspberry Pi powered e-paper frame

## Prerequisites

- [Hardware](https://www.waveshare.net/wiki/10.3inch_e-Paper_HAT)
- [Latest C library for Broadcom BCM 2835 as used in Raspberry Pi](http://www.airspayce.com/mikem/bcm2835/)

```shell
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.70.tar.gz
tar zxvf bcm2835-1.70.tar.gz 
cd bcm2835-1.70/
sudo ./configure
sudo make
sudo make check
sudo make install
```

## Installation

Install by running: `make`

```sh
sudo apt update && sudo apt install -y imagemagick
sudo vim /etc/ImageMagick-6/policy.xml
# Comment out the line prevent pdf: <policy domain="coder" rights="none" pattern="PDF" />
```

## Usage

```shell
sudo ./epd /path/to/file.bmp
```

### Turning off Pi power management

`sudo iwconfig wlan0 power off`
