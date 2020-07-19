import dash

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootswatch/4.5.0/materia/bootstrap.min.css'])
app.title = 'IBMHC'
server = app.server
