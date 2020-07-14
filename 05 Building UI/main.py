import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_auth
from app import app
from app import server
import app1, app2

server = server

VALID_USERNAME_PASSWORD_PAIRS = {
    'admin': 'Root@1234'
}

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div(children=[
    html.Div(id='navbar'),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# @app.server.route('/')
# def go_to_home():
#     return redirect('/index', code=302)

index_page = html.Div(style={'position':'absolute', 'color':'white'}, children=[
    html.Img(
        src='https://www.arcgis.com/sharing/rest/content/items/1924fe844d7a4a98884bd26ea3826760/resources/1574906935648.jpeg?w=3375',
        style={
            'width':'100%',
            # 'height':'20%'
        }
    ),
    html.H1(children='IBM Hack Challenge 2020',
            style={
                'color':colors['background'],
                'textAlign':'center',
                'position':'absolute',
                'top':'7%',
                'left':'50%',
                'transform':'translate(-50%, -50%)',
                'fontSize': '4vw',
                'textDecoration':'underline overline',
                # 'opacity':'0.7'
    }),
    html.H1(children='Predicting the energy output of wind turbine based on weather condition',
            style={
                'color':'black',
                'textAlign':'center',
                'position':'absolute',
                'top':'17%',
                'left':'50%',
                'transform':'translate(-50%, -50%)',
                'fontSize': '2vw',
                # 'textDecoration':'underline',
                # 'opacity':'0.8'
    }),
    html.Br(),
    html.Hr(),
    html.Div("Our Team", style={'fontSize':'3vw', 'color':'black', 'textAlign':'center', 'textDecoration':'underline overline'})
])

@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')])
def update_content(pathname):
    if pathname == '/show_factors':
        return app2.layout

    elif pathname == '/show_predictions':
        return app1.layout
    
    elif pathname == '/':
        return index_page

@app.callback(
    dash.dependencies.Output('navbar', 'children'),
    [dash.dependencies.Input('url', 'pathname')])
def update_content(pathname):
    if pathname == '/show_factors':
        return dbc.Nav(className='breadcrumb',
            children=[
                dbc.NavItem(dbc.NavLink('Homepage', href='/')),
                dbc.NavItem(dbc.NavLink('Show predictions', href='/show_predictions')),
                dbc.NavItem(dbc.NavLink('Show factors', active=True, href='/show_factors')),
            ],
            pills=True,
            fill=True
        )

    elif pathname == '/show_predictions':
        return dbc.Nav(className='breadcrumb',
            children=[
                dbc.NavItem(dbc.NavLink('Homepage', href='/')),
                dbc.NavItem(dbc.NavLink('Show predictions', active=True, href='/show_predictions')),
                dbc.NavItem(dbc.NavLink('Show factors',href='/show_factors')),
            ],
            pills=True, 
            fill=True
        )
    
    elif pathname == '/':
        return dbc.Nav(className='breadcrumb',
            children=[
                dbc.NavItem(dbc.NavLink('Homepage', active=True, href='/')),
                dbc.NavItem(dbc.NavLink('Show predictions', href='/show_predictions')),
                dbc.NavItem(dbc.NavLink('Show factors',href='/show_factors')),
            ],
            pills=True,
            fill=True
        )

if __name__ == '__main__':
    app.run_server(debug=True)