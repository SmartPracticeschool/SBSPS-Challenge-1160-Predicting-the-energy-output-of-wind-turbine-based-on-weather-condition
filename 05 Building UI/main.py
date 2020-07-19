import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_auth
from app_init import app
from app_init import server
import predictions, range_based, date_based, upload_train

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


left_card = html.Div(
    [
        html.H3("Problem Statement", className="card-title"),
        html.P(
            "Wind energy plays an increasing role in the supply of energy world-wide." 
            "The energy output of a wind farm is highly dependent on the wind conditions present at its site." 
            "If the output can be predicted more accurately, energy suppliers can coordinate the collaborative "
            "production of different energy sources more efficiently to avoid costly overproduction."),
        
        html.P(
            "Wind power or wind energy is the use of wind to provide the mechanical power through wind turbines"
            "to turn electric generators and traditionally to do other work, like milling or pumping. Wind power "
            "is a sustainable and renewable energy, and has a much smaller impact on the environment compared to burning "
            "fossil fuels. Wind farms consist of many individual wind turbines, which are connected to the electric power "
            "transmission network. Onshore wind is an inexpensive source of electric power, competitive with or in many places "
            "cheaper than coal or gas plants. Onshore wind farms also have an impact on the landscape, as "
            "typically they need to be spread over more land than other power stations and need to be built in wild "
            "and rural areas, which can lead to industrialization of the countryside and habitat loss. Offshore "
            "wind is steadier and stronger than on land and offshore farms have less visual impact, but construction "
            "and maintenance costs are higher. Small onshore wind farms can feed some energy into the grid or provide "
            "electric power to isolated off-grid locations."
        ),
        dbc.Button("Read More", color="primary" , href="https://smartinternz.com/ibm-hack-challenge-2020"),
    ]
)

right_card = html.Div(
        [
            html.H3("Alerts", className="card-title"),
            html.P(
                "Wind Speed: 340 m/s"
            ),
            html.P(
                "Wind Direction: 43 Deg"
            ),
            html.P(
                "Power Output: 873498"
            ),
            html.H5(
                "Status:"
            ),
            dbc.Button("Active", color="success"),
            html.Br(),
            html.Br(),
            dbc.Button("Detail Predictions", color="warning" , href="/show_predictions"),
        ]
)

info = dbc.Row([dbc.Col(left_card, width=8), dbc.Col(width=1), dbc.Col(right_card, width=3)])

index_page = html.Div(style={'position':'absolute'}, children=[
    
    html.Img(
        src='https://www.arcgis.com/sharing/rest/content/items/1924fe844d7a4a98884bd26ea3826760/resources/1574906935648.jpeg?w=3375',
        style={
            'width':'100%','opacity':'0.7',
            'object-fit': 'cover',
        }
    ),
    html.H1(children='IBM Hack Challenge 2020',
            style={
                'color':colors['background'],
                'textAlign':'center','position':'absolute',
                'top':'27%',
                'left':'50%',
                'transform':'translate(-50%, -50%)',
                'fontSize': '4vw',
                'textDecoration':'underline overline',
            }
    ),
    html.H1(children='Predicting the energy output of wind turbine based on weather condition',
            style={
                'color':'black',
                'textAlign':'center',
                'position':'absolute',
                'top':'37%',
                'left':'50%',
                'transform':'translate(-50%, -50%)',
                'fontSize': '2vw',
                # 'textDecoration':'underline',
                # 'opacity':'0.8'
            }
    ),
    html.P(dbc.Button("Learn more", color="primary", href="/show_factors"), className="lead" , 
            style={
                'color':'black',
                'textAlign':'center',
                'position':'absolute',
                'top':'47%',
                'left':'50%',
                'transform':'translate(-50%, -50%)',
            }
    ),
            
    html.Br(),
    html.Br(),
    html.Br(),
    
    html.Div(className="container", children=[
        info,
        # html.Div("Our Team", style={'fontSize':'3vw', 'color':'black', 'textAlign':'center', 'textDecoration':'underline overline'})
        html.Br(),
        html.Br(),
    ]
    ),
])

@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')])
def update_content(pathname):
    if pathname == '/show_factors':
        return range_based.layout

    elif pathname == '/show_factors_date':
        return date_based.layout

    elif pathname == '/show_predictions':
        return predictions.layout
    
    elif pathname == '/':
        return index_page

    elif pathname == '/retrain':
        return upload_train.layout

@app.callback(
    dash.dependencies.Output('navbar', 'children'),
    [dash.dependencies.Input('url', 'pathname')])
def update_content(pathname):
        if pathname == '/show_factors':
            return navbar
        elif pathname == '/show_factors_date':
            return navbar

        elif pathname == '/show_predictions':
            return navbar
        
        elif pathname == '/retrain':
            return navbar

        elif pathname == '/':
            return navbar
        


"""
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
"""

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", active=True, href='/')),
        dbc.NavItem(dbc.NavLink("Predictions", href="/show_predictions")),
        dbc.NavItem(dbc.NavLink("Visualizations", href="/show_factors")),
        dbc.NavItem(dbc.NavLink("Retrain", href="/retrain")),


    ],
    brand="IBMHC",
    brand_href="#",
    color="dark",
    dark=True,
)


if __name__ == '__main__':
    app.run_server(debug=True)