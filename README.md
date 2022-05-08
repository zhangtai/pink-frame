# pink-frame
Raspberry Pi powered e-paper frame

## Prerequisites

- [Hardware](https://www.waveshare.net/wiki/10.3inch_e-Paper_HAT)
- [Latest C library for Broadcom BCM 2835 as used in Raspberry Pi](http://www.airspayce.com/mikem/bcm2835/)

```shell
export version=1.71
cd /tmp
curl -LO http://www.airspayce.com/mikem/bcm2835/bcm2835-${version}.tar.gz
tar zxvf bcm2835-${version}.tar.gz 
cd bcm2835-${version}
sudo ./configure
sudo make
sudo make check
sudo make install
```

```shell
sudo apt update && sudo apt install -y imagemagick
sudo vim /etc/ImageMagick-6/policy.xml
# Comment out the line prevent pdf: <policy domain="coder" rights="none" pattern="PDF" />
```

## Installation

Clone this repo and install by running: `make`

## Usage

```shell
sudo ./pf /path/to/file.bmp
```

### Turning off Pi power management

`sudo iwconfig wlan0 power off`
