# esp-micropython-stuff

General notes on ESP32 / micropython development.

Board used: _ESP32-WROOM_ and a tiny OLED display

This project includes the [microdot](https://microdot.readthedocs.io/en/latest/intro.html) web framework.

## Toolchain

Espressif toolchain:

```bash
git clone --recursive https://github.com/espressif/esp-idf.git
cd esp-idf
git checkout tags/v5.2.2
git submodule update --init --recursive
./install.sh esp32
. export.sh
```

> :bulb: upstream docs available [here](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/linux-macos-setup.html)

## Micropython firmware

The micropython firmware base:

```bash
git clone https://github.com/micropython/micropython.git
cd micropython
git checkout tags/v1.24.1
make -C mpy-cross
cd ports/esp32
make submodules
make
```

> :bulb: upstream docs available [here](https://github.com/micropython/micropython/blob/v1.24.1/ports/esp32/README.md)

At this point, everything should be fine and a plain micropython firmware should be build and flashed.

## Showtime

```bash
cd ~/dev/micropython/ports/esp32
```

Build, flash and monitor for output:

```bash
idf.py -p /dev/cu.usbserial-0001 build flash monitor
```

> :bulb: the ESP32 is available at `/dev/cu.usbserial-0001`

Custom code goes into `ports/esp32/modules/`, in `main.py` and any additional required modules.

## Console Log

```
[..]
[10/11] Generating binary image from built executable
esptool.py v4.8.1
Creating esp32 image...
Merged 2 ELF sections
Successfully created esp32 image.
Generated #####/micropython/ports/esp32/build/micropython.bin
[..]
micropython.bin binary size 0x190300 bytes. Smallest app partition is 0x1f0000 bytes. 0x5fd00 bytes (19%) free.
Executing action: flash
[..]
esptool.py v4.8.1
Serial port /dev/cu.usbserial-0001
Connecting.....
Chip is ESP32-D0WDQ6 (revision v1.0)
Features: WiFi, BT, Dual Core, 240MHz, VRef calibration in efuse, Coding Scheme None
Crystal is 40MHz
MAC: 84:cc:a8:5f:78:a0
Uploading stub...
Running stub...
Stub running...
Changing baud rate to 460800
Changed.
Configuring flash size...
Flash will be erased from 0x00001000 to 0x00006fff...
Flash will be erased from 0x00010000 to 0x001a0fff...
Flash will be erased from 0x00008000 to 0x00008fff...
SHA digest in image updated
Compressed 23264 bytes to 14544...
Writing at 0x00001000... (100 %)
Wrote 23264 bytes (14544 compressed) at 0x00001000 in 0.8 seconds (effective 238.9 kbit/s)...
Hash of data verified.
Compressed 1639168 bytes to 1098052...
Writing at 0x001a015d... (100 %)
Wrote 1639168 bytes (1098052 compressed) at 0x00010000 in 28.8 seconds (effective 455.7 kbit/s)...
Hash of data verified.
Compressed 3072 bytes to 115...
Writing at 0x00008000... (100 %)
Wrote 3072 bytes (115 compressed) at 0x00008000 in 0.1 seconds (effective 192.3 kbit/s)...
Hash of data verified.

Leaving...
Hard resetting via RTS pin...
Executing action: monitor
Running idf_monitor in directory #####/micropython/ports/esp32
[..]
--- esp-idf-monitor 1.5.0 on /dev/cu.usbserial-0001 115200
--- Quit: Ctrl+] | Menu: Ctrl+T | Help: Ctrl+T followed by Ctrl+H
```
