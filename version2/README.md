# driPies2
A (second) raspberry pi-based watering system. The basic premise is pretty simple: a pump moves water from a reservoir through a series of tubes onto some plants.  This version is a similar design to the previous one, but using a more powerful pump for water pressure, controled via a remote-controlled power socket and incorporating a sensor to warn of a low water level in the reservoir.  The design was based on the environment in which the system operated - to water plants on a balcony with no water tap, but with two power points.  It also incorporates a sensor to warn when the water level in the reservoir is low.

## Hardware

### Pump
I used [this pump](https://www.bunnings.com.au/aquapro-ap550-water-feature-pump_p2810111), together with some [433 MHz radio frequency power outlets](https://www.bunnings.com.au/arlec-remote-controlled-power-outlet-twin-pack_p0095172) and some [433MHz transmitters and receievers](https://www.ebay.com/itm/1X-New-433Mhz-RF-Transmitter-Module-And-Receiver-Link-Kit-For-Arduino-ARM-MCU-WL/182549538034?hash=item2a80cce4f2:g:CFcAAOSw8hxbRvGm).  The RF transmitter and receiever were initially connected to the Pi according to [the documentation for the rpi-rf python module](https://pypi.org/project/rpi-rf/).  However, I didn't have much luck sending codes using this transmitter, so I picked up [this one](https://www.jaycar.com.au/wireless-modules-transmitter-433mhz/p/ZW3100) instead.  It takes 3V input so I used the 3.3V pin instead of 5V, but the rest of the wiring was the same (Data to GPIO pin 17/wiringPi pin 0, ground to ground).

## Software

### Controlling the pump
Somebody [figured out the protocol for the brand of remote I bought](https://github.com/sui77/rc-switch/wiki/Description-of-socket-protocols-from-different-brands-and-models).  I used [SimpleRcScanner](https://github.com/sui77/SimpleRcScanner) to find the codes for my remote.  My remote can control four sockects (A-D), and has two switches for each - one to turn on and one to turn off.  I'm only using one socket (A) for this project. The codes for my remote are in the file `arlec_codes.txt`.  The protocol that worked for me was slighly different than the one previously suggested for the same brand: `{ 350, {  1, 27 }, {  1,  2 }, { 2,  1 }, false }`.

I used the rc-switch library in some c++ code to send my codes.  After compilation with `make`, a 'blink' script turns the socket on and off a couple of times:
```
./sendDemo
```
This script uses the codes and protocol descibed above.  To send just one code:
```
./send 010110100110100100001111000001110
```
