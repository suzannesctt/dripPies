# the RPI variable is needed by rc-switch/RCSwitch.h
CXXFLAGS=-DRPI

all: sendDemo send clean

sendDemo: rc-switch/RCSwitch.o sendDemo.o
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $+ -o $@ -lwiringPi -lwiringPiDev -lcrypt

send: rc-switch/RCSwitch.o send.o
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $+ -o $@ -lwiringPi -lwiringPiDev -lcrypt
clean:
	$(RM) rc-switch/*.o *.o

