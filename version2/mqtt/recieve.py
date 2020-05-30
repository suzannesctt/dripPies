import paho.mqtt.client as mqtt
from datetime import datetime
from sys import argv
from time import sleep
import sqlite3


# constants for calculating fraction of the tank that's full
vair = 343 # velocity of sound in air (m/s)
vwater = 1500 # velocity of sound in water (m/s)
d = 0.55 # total depth of tank (m)

# SQL to insert one or two values
insert_temp = " INSERT INTO temp (temp) VALUES (?)"
insert_humidity = " INSERT INTO humidity (humidity) VALUES (?)"
insert_voltage = " INSERT INTO temp (voltage) VALUES (?)"
insert_usTime = "INSERT INTO tank (ustime, full_pc) VALUES (?,?)"

if argv[1] is None:
    raise ValueError('Please provide a path to database as a command line argument')

# connect to database
conn = sqlite3.connect(argv[1])
c = conn.cursor()

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
        c.execute(insert_usTime, (message, frac_full))
    elif topic == "garden/temperature":
        c.execute(insert_temp, (message))
    elif topic == "garden/humidity":
        c.execute(insert_humidity, (message))
    elif topic == "garden/voltage":
        c.execuite(insert_voltage, (message))
    c.commit()

    print(f"{date} {time} {msg.topic}: {message}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.4", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

c.close()
