/*
Usage: ./send <code> [pin]
pin is according to wiringPi numbering
*/


#include "../rc-switch/RCSwitch.h"
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char * argv[]) {
	// check argc
        if ((argc != 2) && (argc != 3)){
                printf("Sending 433 MHz remote plug control codes\n");
                printf("Usage: %s <code> [pin]\n", argv[0]);
		printf("code - binary code to transmit (without sync bit)\n");
                printf("pin - wiringPi pin number [0]\n");
                return -1;
        }

	// set up wiringPi
        if (wiringPiSetup () == -1) return 1;

	// get code to transmit
	char* code = argv[1];

        // get pin if it was set
        int PIN;
        if (argc == 3) {
                PIN = atoi(argv[2]);
        }
        else {
                PIN = 0;
        }

	//set up switch
	RCSwitch mySwitch = RCSwitch();
	mySwitch.enableTransmit(PIN);
	mySwitch.setRepeatTransmit(3);

	// custom protocol
	static const RCSwitch::Protocol customprotocol = { 350, {  1, 27 }, {  1,  2 }, { 2,  1 }, false };
	mySwitch.setProtocol(customprotocol);

	// transmit
	mySwitch.send(code);
	return 0;
}
