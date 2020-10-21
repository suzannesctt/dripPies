
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import sqlite3
import numpy as np
from datetime import date

db_path = "../data/garden.db"

# tables in database for display
tables = ('temp', 'humidity', 'voltage')
columns = {'temp':'temp', 'humidity':'humidity', 'voltage':'voltage', 'tank':'pc_full'}
labels = {'temp':'Temperature (deg C)',
		'humidity':'Humidity %',
		'voltage':'Voltage (V)',
		'tank': 'Percentage full (%)'
	}

# dash stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# create app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# connect to database
# https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
# this should be fine as long as we don't write using more than one
# (callback) at once
conn = sqlite3.connect(db_path, check_same_thread=False)
c = conn.cursor()

app.layout = html.Div(children=[
	html.H1(children='Garden weather'),
    html.Div([
        dcc.Dropdown(
            options=[
                {'label': 'Temperature', 'value': 'temp'},
                {'label': 'Humidity', 'value': 'humidity'},
                {'label': 'Voltage', 'value': 'voltage'}
            ],
            value='temp',
            id='table-dropdown'
        ),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=date(2020, 10, 21),
            end_date_placeholder_text='Select a date!'
        ),
        dcc.Graph(
            id='graph'
        )
    ])
])


@app.callback(
    Output('graph', 'figure'),
    [Input('table-dropdown', 'value')])
def make_graph(table, date='now'):
	"""Make a graph of data from the last 24 hours"""
	assert table in tables

	# fetch temperature data for the last 24 hours
	if date == 'now':
		iter = c.execute(f"""SELECT {columns[table]}, timestamp
					FROM {table}
					WHERE DATETIME(timestamp) > DATETIME('now', '-7 day');""")
	time = []
	y = []

	# get values from db in list
	for row in iter:
		y.append(row[0])
		time.append(row[1])

	# convert time to numpy dateime64 array
	time = np.array(time, dtype='datetime64')

	# make figure
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=time, y=y, line_shape='spline'))

	return fig

if __name__ == '__main__':
	app.run_server(debug=True)