import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
from app_init import app
import io
import base64
import pandas as pd
# from Predictor import windDirection, windSpeed, Regressor

###### save csv file ############
def save_csv(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    if 'csv' in filename:
    	df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    elif 'xls' in filename:
    	df = pd.read_excel(io.BytesIO(decoded))
    else:
    	return "This file type is not supported"
    df.to_csv("E:\\Projects\\ibm hack challenge\\ibm app\\newdata.csv")
    return "Retrained"

######## save csv file ends ############

######### add training dropdown #####
dropdown = dbc.FormGroup(
    [
        dbc.Label("Mode of training", html_for="dropdown"),
        dcc.Dropdown(
            id="training_mode",
            options=[
                {"label": "Quick Training(relatively less accuracy)", "value": 1},
                {"label": "Satisfactory Training(recommended with tested results)", "value": 2},
                {"label": "Rigourous Training", "value": 3},
            ],
        ),
    ]
)

####### end training dropdown ###########

####### add time slider ########
#create marks dictionary for slider
def get_marks():
    marks = dict()
    for val in range(1, 73):
        marks[val] = '0'+str(val) if val < 10 else str(val)
    return marks

slider = dcc.Slider(
    min=1,
    max=72,
    step=1,
    marks=get_marks(),
    value=1
)
####### end time slider #########

header = html.Div(style={'textAlign':'center', 'marginLeft':'200px', 'fontSize':'25px'}, id="response")
upload_button = dcc.Upload(dbc.Button('Upload File', color="info", style={"float":"right"}), id="upload_file")
train_button = dbc.Button("Train model", color="info", id="trainButton", n_clicks=0, style={"float":"right"})

layout = html.Div(
	style={},
	children=[
		html.Br(),
		dbc.Row([dbc.Col(header, width=6), dbc.Col(upload_button, width=3), dbc.Col(train_button, width=2)]),
		html.Br(),
		html.Div(style={"marginLeft":"10px", "marginRight":"10px"}, children=dropdown),
		html.Br(),
		html.Div(style={}, children=["Prediction hours", slider])
	])

# @app.callback(
# 	Output("make_csv", "children"),
# 	[Input]
# 	)

@app.callback(
	Output("response", "children"),
	[Input("trainButton", "n_clicks"),
	 Input("upload_file", "contents")],
	[State("upload_file", "filename")])
def update_response(btn1, contents, filename):
	changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
	if contents == None:
		message = "Retrain the model"
	else:	
		message = save_csv(contents, filename)
	if 'trainButton' in changed_id:
		return (message)


