import RPi.GPIO as GPIO
import time
import argparse

parser = argparse.ArgumentParser(prog = "water.py", description='Run a pump')
parser.add_argument('--time', type = int, default = 30, required=False, help='how long (in seconds) to run the pump [30]')
parser.add_argument('--pin', type = int, default = 7, required=False, help='GPIO pin to relay [7]')
args = parser.parse_args()

# set GPIO mode
GPIO.setmode(GPIO.BOARD)
channel = args.pin

# set up GPIO board
GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)
time.sleep(1)

# turn on pump
GPIO.output(channel, GPIO.LOW)
time.sleep(args.time)

# turn off pump
GPIO.output(channel, GPIO.HIGH)
time.sleep(1)

# cleanup
GPIO.cleanup()