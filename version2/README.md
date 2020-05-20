# driPies2
A (second) raspberry pi-based watering system. The basic premise is pretty simple: a pump moves water from a reservoir through a series of tubes onto some plants.  This version is a similar design to the previous one, but using a more powerful pump for water pressure, controled via a remote-controlled power socket and incorporating a sensor to warn of a low water level in the reservoir.  The design was based on the environment in which the system operated - to water plants on a balcony with no water tap, but with two power points.  It also incorporates a sensor to warn when the water level in the reservoir is low.

## Hardware

### Pump
I used [this pump](https://www.bunnings.com.au/aquapro-ap550-water-feature-pump_p2810111), together with some [433 MHz radio frequency power outlets](https://www.bunnings.com.au/arlec-remote-controlled-power-outlet-twin-pack_p0095172) and some [433MHz transmitters and receievers](https://www.ebay.com/itm/1X-New-433Mhz-RF-Transmitter-Module-And-Receiver-Link-Kit-For-Arduino-ARM-MCU-WL/182549538034?hash=item2a80cce4f2:g:CFcAAOSw8hxbRvGm).  The RF transmitter and receiever were initially connected to the Pi according to [the documentation for the rpi-rf python module](https://pypi.org/project/rpi-rf/).  However, I didn't have much luck sending codes using this transmitter, so I picked up [this one](https://www.jaycar.com.au/wireless-modules-transmitter-433mhz/p/ZW3100) instead.  It takes 3V input so I used the 3.3V pin instead of 5V, but the rest of the wiring was the same (Data to GPIO pin 17/wiringPi pin 0, ground to ground).

### Outside sensor

Also wanted to be able to know what the conditions were outside on the balcony (for example, if it's hot we might want to water more often), and how much water is left in the tank so the pump doesn't run out (it's submersible, so this would be bad).  But I wanted it to be wireless, to avoid running cables out the door.  So I picked up a [WeMos D1 mini](https://docs.wemos.cc/en/latest/d1/d1_mini.html), [battery shield](https://docs.wemos.cc/en/latest/d1_mini_shiled/battery.html) and [SHT30 shield](https://docs.wemos.cc/en/latest/d1_mini_shiled/sht30.html).  For power, I got a [protected 18650 battery](https://www.jaycar.com.au/18650-2600mah-li-ion-protected-battery/p/SB2299) and [holder](https://www.jaycar.com.au/single-18650-battery-holder/p/PH9205), and some [JST PH 2.0 mm male leads](https://www.amazon.com.au/Shappy-Pieces-Connector-Silicone-Female/dp/B07449V33P).  I also added a [6V, 1W solar panel](https://www.ebay.com.au/itm/Solar-Panel-3-5V-to-18V-Mini-System-0-15W-to-4-2W/132954452525?ssPageName=STRK%3AMEBIDX%3AIT&var=432252785769&_trksid=p2060353.m2749.l2649) and [dfrobot solar lipo charger](https://www.dfrobot.com/product-1139.html) to hopefully avoid the need for ever charging the battery.  For the tank, I got a [waterproof ultrasonic distance sensor](https://www.amazon.com/Waterproof-Ultrasonic-Distance-Measuring-Transducer/dp/B01J5KZU8M/ref=as_li_ss_tl?ie=UTF8&qid=1549537345&sr=8-4&keywords=jsn-sr04t&linkCode=sl1&tag=makerguides-20&linkId=4cf1465a40860d88454c9889f290e594&language=en_US).  

I connected the two shields to the WeMos D1 mini via the supplied header pins, the ultrasonic distance sensor to the WeMos with some [male to male cables](https://www.ebay.com.au/itm/40pc-Dupont-Jump-Wire-Male-To-Male-Jumper-Ribbon-Cable-Lead-Breadboard-Arduino/312018849894?hash=item48a5c5d066:m:mZPu8krz2ptbK4v9815PFAg&var=610781429748).  I connected the 5V, ground, trigger and echo pins on the sensor board to the 5V, ground, D6 and D7 pins on the WeMos, respectivley.  For the power, I soldered a JST male lead to the battery holder, and connected it to the solar lipo charger board.  I soldered some wires to the solar panel and connected them to the 'PWR in' terminals of the solar lipo charger.  I used an old USB micro cable to connect the 'VOUT' terminal of the solar lipo charger board to the battery shield by cutting off the large end to expose the wires, which were screwed into the 'VOUT' terminal.  The USB micro end plugged into the battery shield.

## Software

### Controlling the pump
Somebody [figured out the protocol for the brand of remote I bought](https://github.com/sui77/rc-switch/wiki/Description-of-socket-protocols-from-different-brands-and-models).  I used [SimpleRcScanner](https://github.com/sui77/SimpleRcScanner) to find the codes for my remote.  My remote can control four sockects (A-D), and has two switches for each - one to turn on and one to turn off.  I'm only using one socket (A) for this project. The codes for my remote are in the file `arlec_codes.txt`.  The protocol that worked for me was slighly different than the one previously suggested for the same brand: `{ 350, {  1, 27 }, {  1,  2 }, { 2,  1 }, false }`.

I used the rc-switch library in some c++ code to send my codes.  After compilation with `make`, use the `send` script to turn :
```
./send <code>
```

### Outside sensor

I used MQTT to send messages from the WeMos D1 mini to the raspberry pi.  First, I installed the mosquitto MQTT broker on the pi:
```
sudo apt update
sudo apt-get install mosquitto mosquitto-clients
```
I then configured my mosquitto config file at `/etc/mosquitto/conf.d/mosquitto.conf` with these settings (modified from [here](https://learn.adafruit.com/diy-esp8266-home-security-with-lua-and-mqtt/configuring-mqtt-on-the-raspberry-pi)):

```
max_queued_messages 200
message_size_limit 50
allow_zero_length_clientid true
allow_duplicate_messages false
 
listener 1883
autosave_interval 900
autosave_on_changes false
persistence true
persistence_file mosquitto.db
allow_anonymous true
password_file /etc/mosquitto/passwd
acl_file /etc/mosquitto/acl
```
I then created a password file:

```
sudo mosquitto_passwd -c /etc/mosquitto/passwd suzanne
```

I then created an ACL file `/etc/mosquitto/acl` file that specifes that any user can subscribe but only the user 'suzanne' can publish;
```
# Allow anonymous access to the sys
topic read $SYS/#

# allow suzanne to read and write
user suzanne
topic readwrite garden/#
```
and restarted mosquitto:

```
sudo service mosquitto restart
```

I used the Arduino IDE to upload a sketch to the WeMos D1 mini board.
