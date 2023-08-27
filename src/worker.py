# Show statistics on a generated web page using data from the database

import sqlite3
import time
import datetime
import subprocess
import atexit

# Ping
def ping():
	
	# Ping
	ping = subprocess.Popen(
		["ping", "-c", "1", "1.1.1.1"],
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE
	)
	
	atexit.register(ping.kill)
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



# every minute run the ping function and add the result to the database
while True:
	timestamp, result = ping()
	print("worker.py:",timestamp, result)
	conn = sqlite3.connect('src/ping.db')
	c = conn.cursor()
	c.execute("INSERT INTO ping (timestamp, result) VALUES (?, ?)", (timestamp, result))
	conn.commit()
	conn.close()
	time.sleep(60)
 