/*
Usage: ./sendBinary <code> <pulse>  [pin]
Code is in binary, eg "0101101001101001000011110000011100"
pulse with is in microseconds, eg 415
pin is according to wiringPi numbering
*/



#include "../rc-switch/RCSwitch.h"
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char * argv[]) {
	// check argv
	if (argc < 3){
		printf("Sending 433 MHz remote plug control codes\n");
		printf("Usage: %s <code> <pulseLength> [pin]\n", argv[0]);
		printf("Code - binary code to transmit\n");
		printf("PulseLength - pulse length in microseconds\n");
		printf("pin - wiringPi pin number [0]\n");
		return -1;
	}
	if (wiringPiSetup () == -1) return 1;
	// get pin if it was set
	int PIN;
	if (argc == 4) {
		PIN = atoi(argv[3]);
	}
	else {
		PIN = 0;
	}
	// get pulse length
	int PULSE = atoi(argv[2]);

	// get code to transmit from argv
	const char* code = argv[1];



	// set up switch
	static const RCSwitch::Protocol customprotocol = { 105, {  3, 99 }, {  3,  8 }, { 8,  3 }, false };
	RCSwitch mySwitch = RCSwitch();
	mySwitch.enableTransmit(PIN);
	mySwitch.setPulseLength(PULSE);
	mySwitch.setProtocol(customprotocol);

	// send codes
	mySwitch.send(code);


}
	
