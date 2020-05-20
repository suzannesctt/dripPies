/*
Test of 433 MHz transmitter - repeats sending two codes (on and off) twice
Codes and protocol are hard-coded
Usage: ./sendDemo [pin]
pin is according to wiringPi numbering
*/


#include "rc-switch/RCSwitch.h"
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

int main(int argc, char * argv[]) {


	// check argv
        if (argc > 2){
                printf("Sending 433 MHz remote plug control codes\n");
                printf("Usage: %s [pin]\n", argv[0]);
                printf("pin - wiringPi pin number [0]\n");
                return -1;
        }

	// set up wiringPi
        if (wiringPiSetup () == -1) return 1;

        // get pin if it was set
        int PIN;
        if (argc == 2) {
                PIN = atoi(argv[1]);
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
	int REPEAT = 2;
	int i = 0;
	while (i < REPEAT) {
		mySwitch.send("010110100110100100001111000001110");
		sleep(1);
		mySwitch.send("010110100110100100001110000001100");
		sleep(1);
		i++;
	}
	return 0;
}
