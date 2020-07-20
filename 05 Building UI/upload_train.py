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
                {"label": "Quick Training (Low Accuracy)", "value": 1},
                {"label": "Satisfactory Training (Recommended Medium Accuracy)", "value": 2},
                {"label": "Rigourous Training (High Accuracy)", "value": 3},
            ],
        ),
    ]
)

####### end training dropdown ###########


header = html.Div(style={'fontSize':'25px'}, id="response")
upload_button = dcc.Upload(dbc.Button('Upload File', color="info",), id="upload_file")
train_button = dbc.Button("Train model", color="info", id="trainButton", n_clicks=0, )
predictions_button = dbc.Button("See Predictions", color="success" , href="/show_predictions")

card = dbc.Card(
    dbc.CardBody(
        [
            html.H2("Training Models", className="card-title"),
            html.H6("To keep the model Renewed and for getting better predictions keep retraining the model with new values. Just select the mode of", className="card-text"),
            html.H6("training according to your need. Upload the CSV file with new data point and Click on Train Model", className="card-text"),
        
            # html.P(
            #     "To keep the model Renewed and for getting better predictions ",
            #     "keep retraining the model with new values. Just select the mode of",
            #     " training according to your need. Upload the CSV file with new ",
            #     "data point and Click on Train Model",
            #     className="card-text",
            # ),

            html.Br(),
            html.Div(style={"marginLeft":"10px", "marginRight":"10px"}, children=dropdown),
            html.Br(),
            dbc.Row([ dbc.Col(upload_button, width=6), dbc.Col(train_button, width=6)]),
            html.Br(),
            dbc.Row([ dbc.Col(header, width=8), dbc.Col(predictions_button,width=4)]),
        
            # dbc.CardLink("Card link", href="#"),
            # dbc.CardLink("External link", href="https://google.com"),
        ]
    ),
    style={"width": "18rem" , 
    'textAlign':'center', 
    },
    className="w-100 mb-4",
)

layout = html.Div(className="container",style={},
	children=[
		html.Br(),html.Br(),
        card,
	]
)

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
		message = "Training Successful !!!"
	else:	
		message = save_csv(contents, filename)
	if 'trainButton' in changed_id:
		return (message)


