# imports
import RPi.GPIO as GPIO
from time import sleep
from functools import partial

def main():
	#pin to use for output
	PIN=17  # using bcm numbering

	# timings
	timings = {}
	timings["pulse_length"] = 350	#pulse length in microseconds
	timings["zero"] = [1,2]		#a zero is on for 1x pulse length and off for 2x pulse length
	timings["one"] = [2,1]		# a one is on for 2x pulse length and off for 1x pulse length
	timings["sync"] = [1, 27]	# sync bit, added after the last data bit 

	# codes - not including sync bit
	a_on="010110100110100100001111000001110"
	b_on="010110100110100100001101000001010"
	c_on="010110100110100100001011000000110"
	d_on="010110100110100100000111000010110"

	a_off="010110100110100100001110000001100"
	b_off="010110100110100100001100000001000"
	c_off="010110100110100100001010000000100"
	d_off="010110100110100100000110000010100"

	all_on="010110100110100100000100000010000"
	all_off="010110100110100100001000000000000"


	# use board numbering
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(PIN, GPIO.OUT)
	i = 0
	while (i < 3):
		countdown(3)
		print(f"sending {a_on}")
		transmit(a_on, timings, PIN)
		countdown(3)
		print(f"sending {a_off}")
		transmit(a_off, timings, PIN)
		i = i+1
	GPIO.cleanup()

def test_sleep(code, protocol, repeats=3):
	# construct lengths for bits
	zero = [length*protocol["pulse_length"] for length in protocol["zero"]]
	one = [length*protocol["pulse_length"] for length in protocol["one"]]
	sync = [length*protocol["pulse_length"] for length in protocol["sync"]]
	# construct code
	do_code = []
	for digit in code:
		if digit == "1":
			do_code.append(partial(print, "1", end="", flush=True))
			do_code.append(partial(sleep, 0.1))
		elif digit == "0":
			do_code.append(partial(print, "0", end="", flush=True))
			do_code.append(partial(sleep, 0.1))
		else:
			raise ValueError("Unregconised digit")
	do_code.append(partial(print, "sync", end="", flush=True))
	do_code.append(partial(sleep, 0.1))
	do_code.append(partial(print, "", flush=True))

	[func() for func in do_code]


# func for transmission
def transmit(code, protocol, pin, repeats=3):
	# construct lengths for bits
	usec = 1000000
	zero = [length*protocol["pulse_length"]/usec for length in protocol["zero"]]
	one = [length*protocol["pulse_length"]/usec for length in protocol["one"]]
	sync = [length*protocol["pulse_length"]/usec for length in protocol["sync"]]
	# construct code
	do_code = []
	for digit in code:
		if digit == "0":
			do_code.append(partial(GPIO.output, pin, GPIO.HIGH))
			do_code.append(partial(sleep, zero[0]))
			do_code.append(partial(GPIO.output, pin, GPIO.LOW))
			do_code.append(partial(sleep, zero[1]))
		elif digit == "1":
			do_code.append(partial(GPIO.output, pin, GPIO.HIGH))
			do_code.append(partial(sleep, one[0]))
			do_code.append(partial(GPIO.output, pin, GPIO.LOW))
			do_code.append(partial(sleep, one[1]))
		else:
			raise ValueError("Bad code: Codes must consist of '1' and '0' only!")
	# add sync bit
	do_code.append(partial(GPIO.output, pin, GPIO.HIGH))
	do_code.append(partial(sleep, sync[0]))
	do_code.append(partial(GPIO.output, pin, GPIO.LOW))
	do_code.append(partial(sleep, sync[1]))

	# set up repeats
	do_code = do_code*repeats

	# execute code
	[func() for func in do_code]

def countdown(sec):
	if sec < 0 :
		return
	elif sec > 5:
		sec = 5
	while sec > 0:
		print(f"{sec}... ", end="", flush=True)
		sleep(1)
		sec -= 1
	print("")
	return

if __name__ == "__main__":
	main()
