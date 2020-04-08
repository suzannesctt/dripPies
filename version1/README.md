# DripPi

A Raspberry Pi-based watering system

## Hardware

Had 10 plants to water, so I used two pumps and rigged up tubing to drip onto each one.

### Pump(s)

Roughly followed [Ben Eagan's design](https://www.hackster.io/ben-eagan/raspberry-pi-automated-plant-watering-with-website-8af2dc) for the pump, but skipped the water sensor because apparently they corrode pretty quickly.  Used [this pump](https://core-electronics.com.au/mute-sounds-mini-submersible-pump-dc-3v-5v.html) and [this relay](https://core-electronics.com.au/5v-4-channel-relay-module-10a.html).  The comments for the relay suggest that it doesn't work with RPi GPIO pins because the voltage they provide is too low to activate the switch, but it seemed to work for me.  As in Ben's design, I used two old USB cables and a USB wall plug (5V, 2.4A) to power the pumps.  Each pump had its own power cable.

### Tubing
Used some [4mm diameter irrigation tubing](https://www.bunnings.com.au/holman-4mm-x-10m-irrigation-drip-flex-tube_p3120586) that I had lying around, together with some [4mm barbed T and cross juctions](https://www.popeproducts.com.au/irrigation/poly-fittings/4-mm-fittings) to connect it.  Plugged the end of the tubing with [4mm repair plugs](https://www.bunnings.com.au/pope-4mm-repair-plug-40-pack_p3120432), and then poked small holes for the water to drip out of to make drippies. Needed some larger tubing, [6mm and 3mm](https://www.popeproducts.com.au/hoses/clear-vinyl-tubing-and-clear-vinyl-joiners) to connect the pump to the 4mm tubing. 

Rigged up the tubing to water 5 plants per pump.  Tied the plugged ends of the tubing to skewers to anchor drippies at each plant.

## Code

As a first step, wrote some python code to turn the pump on for a set amount of time.  To run:  
```
python3 src/water.py --time <time in seconds> --pin <GPIO pin (GPIO.BOARD)>
```

Scheduled this to run three times a week using `crontab` \(`crontab -e`\):  
```
0,10,20,30,40,50 12 * * tue,thu,sat ~/Documents/drippies/src/water.py --time 120 --pin 7
0,10,20,30,40,50 13 * * tue,thu,sat ~/Documents/drippies/src/water.py --time 240 --pin 11
```
Since I'm using each pump for five drippies, and the pump isn't that powerful, it needs to stay on for several minutes to wet the soil properley.  I'm not sure how resilient the pump is, so I'm running it for a few minutes at a time over the course of an hour.  One of the pumps seems to be better than the other, so the better one runs for less time.
