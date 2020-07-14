# import modules
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from datetime import datetime as dt
import re
from app import app

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# Filter data based on two dates
def filter_data_based_on_dates(date1, date2, df):
    date1 = date1.split('-')
    date2 = date2.split('-')
    date1[1] = date1[1].lstrip('0')
    date1[2] = date1[2].lstrip('0')
    date2[1] = date2[1].lstrip('0')
    date2[2] = date2[2].lstrip('0')
    date1 = '-'.join(date1)
    date2 = '-'.join(date2)
    data = df[df['date'] >= date1]
    data = data[data['date'] <= date2]
    return data

# filter data based on number of hours of a particular day
def filter_data_based_on_hours(date, from_hour, to_hour, df):    
    date = date.split()[0]
    date = date.split('-')
    date[1] = date[1].lstrip('0')
    date[2] = date[2].lstrip('0')
    date = '-'.join(date)
    data = df[df['date'] == date]
    hour_list = list()
    for hour in range(from_hour, to_hour):
        hour_list.append('0'+str(hour) if hour < 10 else str(hour))
    data = data[data.hour.isin(hour_list)]
    return data

#create marks dictionary for slider
def get_marks():
    marks = dict()
    for val in range(25):
        marks[val] = '0'+str(val)+':00' if val < 10 else str(val)+':00'
    return marks

#load data into a dataframe
url = 'https://gist.githubusercontent.com/TechTarun/3497b164548f3c7d7a400b2af3c76fdf/raw/be0fd8f8a1b10cf922c137cc1810da6f5b332c09/data.csv'
df = pd.read_csv(url)
# df = pd.read_csv('E:\\Projects\\ibm hack challenge\\ibm app\\apps\\data.csv')
df['date'] = pd.to_datetime(df['date'])

# Create traces
#graph 1
def create_total_figure(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Date/Time'],
        y=df['Theoretical_Power_Curve (KWh)'],
        mode='lines',
        name='Theoretical_Power_Curve (KWh)',
        marker=dict(symbol="circle", color="green")))

    fig.add_trace(go.Scatter(
        x=df['Date/Time'],
        y=df['LV ActivePower (kW)'],
        mode='lines',
        name='LV ActivePower (kW)',
        opacity=0.7,
        marker=dict(symbol="triangle-up-dot", color="red")))

    fig.update_layout(
        # plot_bgcolor=colors['background'],
        paper_bgcolor='#AFEEEE', 
        font_color=colors['background'],
        title='Variation in Theoretical power and LV Active power within a time period',
        xaxis_title="Timeline",
        # font=dict(
        #     family="Courier New, monospace",
        #     size=13,
        #     color=colors['background'],

        # ),
    )
    return fig

#graph 2
def create_daily_figure(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['time'],
        y=df['Theoretical_Power_Curve (KWh)'],
        mode='markers+lines',
        name='Theoretical_Power_Curve (KWh)',
        marker=dict(symbol="circle", color="green")))

    fig.add_trace(go.Scatter(
        x=df['time'],
        y=df['LV ActivePower (kW)'],
        mode='markers+lines',
        name='LV ActivePower (kW)',
        opacity=0.7,
        marker=dict(symbol="circle", color="red")))

    fig.update_layout(
        # plot_bgcolor=colors['background'],
        paper_bgcolor='#AFEEEE', 
        font_color=colors['background'],
        title='Variation in Theoretical power and LV Active power on a specific date',
        xaxis_title="Timeline",
        # font=dict(
        #     family="Courier New, monospace",
        #     size=13,
        #     color=colors['background']
        # ),
    )
    return fig

# graph 3
def create_wind_speed_total(df):
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'polar'}, {'type': 'xy'}]])

    fig.add_trace(go.Scatterpolargl(
          r = df['Wind Speed (m/s)'],
          theta = df['Wind Direction (°)'],
          name = "Wind Speed",
          marker=dict(size=2, color="mediumseagreen"),
          mode="markers"
        ),
        row=1,
        col=1)

    fig.add_trace(go.Histogram(
        x = df['Wind Speed (m/s)'],
        nbinsx=26,
        name='wind speed',
        marker_color='mediumseagreen'
        ),
        row=1,
        col=2
    )

    fig.update_layout(
        title='Variation in wind speed with direction within a specific time period',
        paper_bgcolor='#AFEEEE',
        )
    # fig.update_traces(mode="markers")
    return fig

def create_wind_speed_daily(df):
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'polar'}, {'type': 'xy'}]])

    fig.add_trace(go.Scatterpolargl(
          r = df['Wind Speed (m/s)'],
          theta = df['Wind Direction (°)'],
          name = "Wind Speed",
          marker=dict(size=4, color="darkorange"),
          mode="markers"
        ),
        row=1,
        col=1)

    fig.add_trace(go.Histogram(
        x = df['Wind Speed (m/s)'],
        nbinsx=26,
        name='wind speed',
        marker_color='darkorange'
        ),
        row=1,
        col=2
    )

    fig.update_layout(
        title='Variation in wind speed with direction on a specific date',
        paper_bgcolor='#AFEEEE',
        )
    # fig.update_traces()
    return fig

# App layout for this page
layout = html.Div(children=[
    html.Br(),
    html.H3(
        children='Various factors affecting power output',
        style={
            'textAlign': 'center',
            'color': colors['background'],
            'fontWeight': 900
        }
    ),
    html.Br(),
    html.Div(children=[
        # Graph 1
        html.H4(
            children='Time-period based visualization',
            style={
            'textAlign':'center',
            'color':'black',
            'fontWeight': 700
            }),
        html.Div(style={'margin-left' : '15px', 'float' : 'inherit'},children=["Date Range : ",
        dcc.DatePickerRange(
            style={"margin-left": "15px"},
            id='selection_based_on_dates',
            min_date_allowed=dt(2018, 1, 1),
            max_date_allowed=dt(2018, 12, 31),
            start_date_placeholder_text="Start Date",
            end_date_placeholder_text="End Date",
            display_format='D/M/Y',
            month_format='MMM Do, YY',
            with_portal=True,
            start_date=dt(2018, 1, 1),
            end_date=dt(2018, 1, 31)
        )]),
        html.Br(),
        html.Div(id='output_visualization_total'),
        html.Hr(),
        html.Div(id='output_total_windspeed')
    ]),
    html.Br(),
    html.Hr(),
    html.Hr(),
    html.Div(children=[
        # Graph 2
        html.H4(
            children='Time-period based visualization for a specific date',
            style={
            'textAlign':'center',
            'color':'black',
            'fontWeight': 700
            }),
        html.Div(style={'margin-left' : '15px'},children=[
        "Select Date : ",
        dcc.DatePickerSingle(
            style={"margin-left": "15px"},
            id='selection_based_on_hours',
            min_date_allowed=dt(2018, 1, 1),
            max_date_allowed=dt(2018, 12, 31),
            display_format='D/M/Y',
            month_format='MMM Do, YY',
            with_portal=True,
            date=str(dt(2018, 1, 1))
        )]),
        html.Br(),
        html.Div(style={'margin-left' : '15px'},children=[
        "Select Time Range (in 24-hour format) : ",
        dcc.RangeSlider(
            id='time_range',
            min=0,
            max=24,
            allowCross=False,
            step=1,
            marks=get_marks(),
            value=[0, 24]
        )]),
        html.Div(id='output_visualization_daybase'),
        html.Hr(),
        html.Div(id='output_daywise_windspeed')
    ]),
    html.Br(),
    html.Hr(),
    html.Hr(),
])

@app.callback(
    dash.dependencies.Output('output_visualization_total', 'children'),
    [dash.dependencies.Input('selection_based_on_dates', 'start_date'),
     dash.dependencies.Input('selection_based_on_dates', 'end_date')])
def update_total_graph(start_date, end_date):
    data = filter_data_based_on_dates(start_date, end_date, df)
    fig = create_total_figure(data)
    return dcc.Graph(
        id='total_graph',
        figure=fig
        )

@app.callback(
    dash.dependencies.Output('output_total_windspeed', 'children'),
    [dash.dependencies.Input('selection_based_on_dates', 'start_date'),
     dash.dependencies.Input('selection_based_on_dates', 'end_date')])
def update_total_windspeed_graph(start_date, end_date):
    data = filter_data_based_on_dates(start_date, end_date, df)
    fig = create_wind_speed_total(data)
    return dcc.Graph(
        id='total_windspeed_graph',
        figure=fig
        )

@app.callback(
    dash.dependencies.Output('output_visualization_daybase', 'children'),
    [dash.dependencies.Input('selection_based_on_hours', 'date'),
    dash.dependencies.Input('time_range', 'value')])
def update_total_daywise(date, value):
    data = filter_data_based_on_hours(date, value[0], value[1], df)
    fig = create_daily_figure(data)
    return dcc.Graph(
        id='daily_graph',
        figure=fig
        )

@app.callback(
    dash.dependencies.Output('output_daywise_windspeed', 'children'),
    [dash.dependencies.Input('selection_based_on_hours', 'date'),
    dash.dependencies.Input('time_range', 'value')])
def update_total_daywise(date, value):
    data = filter_data_based_on_hours(date, value[0], value[1], df)
    fig = create_wind_speed_daily(data)
    return dcc.Graph(
        id='daily_windspeed_graph',
        figure=fig
        )
