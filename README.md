# Drippies

A Raspberry Pi-based watering system

## Hardware

Roughly followed [Ben Eagan's design](https://www.hackster.io/ben-eagan/raspberry-pi-automated-plant-watering-with-website-8af2dc) for the pump, but skipped the water sensor because apparently they corrode pretty quickly.
Used some [4mm diameter irrigation tubing](https://www.bunnings.com.au/holman-4mm-x-10m-irrigation-drip-flex-tube_p3120586) that I had lying around, together with some [4mm barbed T and cross juctions](https://www.popeproducts.com.au/irrigation/poly-fittings/4-mm-fittings) to connect it. Needed some larger tubing, [6mm and 3mm](https://www.popeproducts.com.au/hoses/clear-vinyl-tubing-and-clear-vinyl-joiners) to connect the pump to the 4mm tubing. 

## Code

As a first step, wrote some python 3 code to turn the pump on for a set amount of time.  To run:  
```
python3 src/water.py --time <time in seconds> --pin <GPIO pin (GPIO.BOARD)>
```

Scheduled this to run twice a week using `crontab` \(`crontab -e`\):  
```
0 12 * * sun,wed ~/Documents/drippies/src/water.py --time 120 --pin 7
```

