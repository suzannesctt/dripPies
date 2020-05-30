import paho.mqtt.client as mqtt
from datetime import datetime
from sys import argv
from time import sleep


# constants for calculating fraction of the tank that's full
vair = 343 # velocity of sound in air (m/s)
vwater = 1500 # velocity of sound in water (m/s)
d = 0.55 # total depth of tank (m)


if argv[1] is None:
    raise ValueError('Please provide a path to save files as a command line argument')

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("garden/temperature")
    client.subscribe("garden/humidity")
    client.subscribe("garden/usTime")
    client.subscribe("garden/voltage")



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    topic = msg.topic
    message = msg.payload.decode('utf-8')
    time = datetime.today().strftime('%H:%M:%S')
    date = datetime.today().strftime('%Y-%m-%d')
    # if the topic is usTime, convert to fraction of the tank that's full
    if topic == "garden/usTime":
        sec = int(message)/1000000
        frac_full = (vair*vwater*sec - 2*d*vwater)/(2*d*vair - 2*d*vwater)
        print(f"{date} {time} {msg.topic}: {message} ({frac_full*100}% full)")
    else:
        print(f"{date} {time} {msg.topic}: {message}")
    filename = f"{argv[1]}/{date}_{msg.topic.split('/')[1]}.txt"
    with open(filename, "a+") as handle:
        if topic == "garden/usTime":
            handle.write(f"{time}\t{message}\t{frac_full}\n")
        else:
            handle.write(f"{time}\t{message}\n")



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.4", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
