import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import pandas as pd
from app_init import app
import numpy as np

####### load the data ########
url = 'https://drive.google.com/file/d/1-1xB5H5D17zyCheRphDYz7D5C98jbk0I/view?usp=sharing'
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
df = pd.read_csv(path)

####### helper functions #########
def plot_wind_speed(df):
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'polar'}, {'type': 'xy'}]])

    fig.add_trace(go.Scatterpolargl(
          r = df['Wind Speed (m/s)'],
          theta = df['Wind Direction (°)'],
          name = "Wind Speed",
          marker=dict(size=5, color="mediumseagreen"),
          mode="markers"
        ),
        row=1,
        col=1)

    fig.add_trace(go.Scatter(
        x=get_hours(),
        y=df['Wind Speed (m/s)'],
        mode='lines+markers',
        name='Theoretical_Power_Curve (KWh)',
        marker=dict(symbol="circle", color="mediumseagreen"))
    )

    fig.update_layout(
        title='Predicted wind speed and wind direction for next 72 hrs.',
        paper_bgcolor='#AFEEEE',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="LightSteelBlue",
            bordercolor="Black",
            borderwidth=2
        ),
        xaxis_title='Time (in hours)',
        yaxis_title='Wind Speed(m/s)'
        )
    return fig

def plot_predicted_power(df):
	fig = go.Figure()

	fig.add_trace(
		go.Scatter(
			x=get_hours(),
			y=df['LV ActivePower (kW)'],
			mode='lines+markers',
			name='Predicted Active Power (kW)',
			marker=dict(
				symbol='circle',
				color='darkorange'
			)
		)
	)

	fig.update_layout(
        title='Predicted LV Active Power Output for next 72 hrs.',
        paper_bgcolor='#AFEEEE',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="LightSteelBlue",
            bordercolor="Black",
            borderwidth=2
        ),
        xaxis_title='Time (in hours)',
        yaxis_title='Active Power(kW)'
    )

	return fig

def get_hours():
	hours = np.arange(72)
	return hours

##### helper function ends #########

####### app layout #########
header = html.Div("Predictions for next 72 hrs.", style={'textAlign':'center', 'marginLeft':'200px', 'fontSize':'25px'})
Button = dbc.Button("Update Predictions", color="info" , href="/show_predictions")

layout = html.Div(children=[
    html.Br(),
    dbc.Row([dbc.Col(header , width=10),dbc.Col(Button, width=2)]),
    html.Br(),
	html.Div(id='active power graph', children=[
		dcc.Graph(figure=plot_predicted_power(df))
	]),
	html.Div(id='wind speed and direction graph', children=[
		dcc.Graph(figure=plot_wind_speed(df))
	])

])

