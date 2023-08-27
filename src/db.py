import sqlite3
import os
import time
import datetime
import subprocess


def ping():
	
	# Ping
	ping = subprocess.Popen(
		["ping", "-c", "1", "1.1.1.1"],
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE
	)
 
	# Get output
	out, error = ping.communicate()
	
	# Get timestamp
	timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
	
	# Get result
	if "1 packets transmitted, 1 received, 0% packet loss" in out.decode('utf-8'):
		result = "Success"
	else:
		result = "Failure"
	
	# Return timestamp and result
	return timestamp, result



# Create database if it doesn't exist
if not os.path.exists('src/ping.db'):
    
	timestamp, result = ping()
	print(timestamp, result)
 
 
	conn = sqlite3.connect('src/ping.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE ping (id INTEGER PRIMARY KEY, timestamp TEXT, result TEXT)''')
	c.execute("INSERT INTO ping (timestamp, result) VALUES (?, ?)", (timestamp, result))
	conn.commit()
	conn.close()
else:
    quit(0)
    