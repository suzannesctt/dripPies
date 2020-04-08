# driPies2
A (second) raspberry pi-based watering system. The basic premise is pretty simple: a pump moves water from a reservoir through a series of tubes onto some plants.  This version is a similar design to the previous one, but using a more powerful pump for water pressure, controled via a remote-controlled power socket and incorporating a sensor to warn of a low water level in the reservoir.  The design was based on the environment in which the system operated - to water plants on a balcony with no water tap, but with two power points.  It also incorporates a sensor to warn when the water level in the reservoir is low.

## Hardware

### Pump
I used [this pump](https://www.bunnings.com.au/aquapro-ap550-water-feature-pump_p2810111), together with some [433 MHz radio frequency power outlets](https://www.bunnings.com.au/arlec-remote-controlled-power-outlet-twin-pack_p0095172) and some [433MHz transmitters and receievers](https://www.ebay.com/itm/1X-New-433Mhz-RF-Transmitter-Module-And-Receiver-Link-Kit-For-Arduino-ARM-MCU-WL/182549538034?hash=item2a80cce4f2:g:CFcAAOSw8hxbRvGm).  The RF transmitter and receiever were connected to the Pi according to [the documentation for the rpi-rf python module](https://pypi.org/project/rpi-rf/).
