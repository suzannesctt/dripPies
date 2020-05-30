import sqlite3

# connect to database
conn = sqlite3.connect('../data/garden.db')

# create a table for the temperature
# dates should be in ISO 8601 format
temp = """CREATE TABLE temp
		(id INTEGER PRIMARY KEY,
		 temp  REAL,
		 timestamp DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'NOW', 'localtime'))
		 )
	"""

# similar table for humidity
humidity = """CREATE TABLE humidity 
                (id INTEGER PRIMARY KEY,
                 humidity  REAL,
		 timestamp DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'NOW', 'localtime'))
                 )
        """

# similar table for voltage
voltage = """CREATE TABLE voltage 
                (id INTEGER PRIMARY KEY,
                 voltage  REAL,
		 timestamp DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'NOW', 'localtime'))
                 )
        """

# tank table has two columns - time in us between trigger and echo, and percentage full
tank = """CREATE TABLE tank 
                (id INTEGER PRIMARY KEY,
recieve.py                 ustime INTEGER,
		 full_pc  REAL,
		 timestamp DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'NOW', 'localtime'))
		 )
        """

# watering table to keep track of when last watered and for how long
water = """CREATE TABLE water
		(id INTEGER PRIMARY KEY,
		 timestamp_start DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'NOW', 'localtime')),
		 duration_sec INTEGER
		)
	"""

c = conn.cursor()

c.execute(temp)
c.execute(humidity)
c.execute(voltage)
c.execute(tank)
c.execute(water)

conn.commit()

conn.close()
