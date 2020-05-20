# the RPI variable is needed by rc-switch/RCSwitch.h
CXXFLAGS=-DRPI

all: send clean

send: ../rc-switch/RCSwitch.o send.o
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $+ -o $@ -lwiringPi -lwiringPiDev -lcrypt
clean:
	$(RM) ../rc-switch/*.o *.o

