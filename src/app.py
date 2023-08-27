import sqlite3
import os
import subprocess
from flask import Flask, jsonify, stream_template 


# Initialize Flask app
app = Flask(__name__)

# get last id from database
def get_last_id():
	conn = sqlite3.connect('src/ping.db')
	c = conn.cursor()
	c.execute("SELECT id FROM ping ORDER BY id DESC LIMIT 1")
	last_id = c.fetchone()
	conn.close()
 
	if last_id == None:
		return 1
	
	return last_id[0]

def get_num_failed():
	conn = sqlite3.connect('src/ping.db')
	c = conn.cursor()
	c.execute("SELECT COUNT(*) FROM ping WHERE result='Failure'")
	num_failed = c.fetchone()
	conn.close()
	return num_failed[0]

def get_num_success():
    total = get_last_id()
    failed = get_num_failed()
    success = total - failed
    return success

def get_success_rate():
	total = get_last_id()
	failed = get_num_failed()
	success = total - failed
	rate = success / total * 100

	# get number of characters in success and failure and get the number of decimal places of the greater number
	if success > failed:
		decimal_places = len(str(success))
	else:
		decimal_places = len(str(failed))

	return round(rate, decimal_places)

def get_external_ip():
	external_ip = os.popen('dig @resolver4.opendns.com myip.opendns.com +short').readline()
	
	# Remove trailing newline
	external_ip = external_ip.rstrip()
	return external_ip

def get_isp_name():
    
	bash_command = """ 
		wget '--header=User-Agent: Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11' -q -O - whoismyisp.org | grep -oP -m1 '(?<=block text-4xl\">).*(?=</span)'
	"""
    
	isp_name = os.popen(bash_command).readline()
	isp_name = isp_name.rstrip()
	return isp_name

def running_since():
	conn = sqlite3.connect('src/ping.db')
	c = conn.cursor()
	c.execute("SELECT timestamp FROM ping ORDER BY id ASC LIMIT 1")
	running_since = c.fetchone()
	conn.close()
	return running_since[0]

# return the last time the time between pings was more than 2 minutes
def get_last_time():
	conn = sqlite3.connect('src/ping.db')
	c = conn.cursor()
	c.execute("SELECT timestamp FROM ping WHERE id = (SELECT MAX(id) FROM ping WHERE timestamp < datetime('now', '-2 minutes'))")
	last_time = c.fetchone()
	conn.close()
	return last_time[0]

print("Rate: " + str(get_success_rate()))
print("Num. Entries: " + str(get_last_id()))
print("Failed: " + str(get_num_failed()))
print("Success: " + str(get_num_success()))
print("External IP: " + str(get_external_ip()))
print("ISP Name: " + str(get_isp_name()))
print("Running since: " + str(running_since()))
print("Last time: " + str(get_last_time()))


subprocess.Popen(["python3", "src/worker.py"])

# Flask template for stats to show graph

@app.route("/")
def stats(title=None, uptime=None, total=None, failure=None, success=None, external_ip=None, isp_name=None):
	return stream_template('stats.html', title='Stats', uptime=get_success_rate(), total=get_last_id(), failure=get_num_failed(), success=get_num_success(), external_ip=get_external_ip(), isp_name=get_isp_name())

@app.route("/api")
def api(uptime=None, total=None, failure=None, success=None, external_ip=None, isp_name=None):
	return jsonify(uptime=get_success_rate(), total=get_last_id(), failure=get_num_failed(), success=get_num_success(), external_ip=get_external_ip(), isp_name=get_isp_name())

app.run(debug=True, host='localhost', port=5000, use_reloader=False)
