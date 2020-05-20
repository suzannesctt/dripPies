from flask import Flask, render_template
import datetime
import subprocess
import yaml
from os import path

app = Flask(__name__)
YAML_PATH="codes/codes.yml"

# load codes from yaml
with open(YAML_PATH, 'r') as stream:
	try:
		codes = yaml.safe_load(stream)
	except yaml.YAMLError as exc:
		print(exc)

# check that the script exists
if not(path.exists(codes['script_path'])):
	raise OSError("Script for sending codes does not exist")

# turn everything off
command = [codes['script_path'], codes['remote']['all']['off']]
subprocess.run(command)

# add status field to dictionaries for A, B, C, D
for field in codes['remote']['plugs'].keys():
	codes['remote']['plugs'][field]['status'] = False
# data structure for pages
templateData = {
  'title' : "driPies v2",
  'time'  : "",
  'status': { plug:False for plug in codes['remote']['plugs'].keys() }
          }

# function for getting time
def get_time():
	now = datetime.datetime.now()
	return now.strftime("%Y-%m-%d %H:%M")

# home page
@app.route('/')
def index():
	# update time
	templateData['time'] = get_time()
	return render_template('main.html', **templateData)

@app.route('/<plug>/<action>')
def action(plug, action):
	# if the plug is not valid, return homepage
	if plug not in ['A', 'B', 'C', 'D', 'all']:
		return render_template('main.html', **templateData)
	if action not in ['on', 'off']:
		return render_template('main.html', **templateData)

	# switch on or off
	if plug == "all":
		command = [codes['script_path'], codes['remote']['all'][action]]
		for curr_plug in codes['remote']['plugs'].keys():
			codes['remote']['plugs'][curr_plug]['status'] = \
			  True if action == 'on' else False
	else:
		command = [codes['script_path'], codes['remote']['plugs'][plug][action]]
		codes['remote']['plugs'][plug]['status'] = \
		  True if action == 'on' else False

	subprocess.run(command)

	# get message to display
	message = f"Turned {plug} {action}"

	# update templateData
	templateData['time'] = get_time()
	templateData['status'] = { plug:codes['remote']['plugs'][plug]['status'] for plug \
		in codes['remote']['plugs'].keys() }
	templateData['message'] = message
	print(templateData)
	return render_template('main.html', **templateData)
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
