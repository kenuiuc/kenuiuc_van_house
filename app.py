from dash import dash, html

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
server = app.server

app.layout = html.Div([
    html.H1('Hi Ken')
])

if __name__ == '__main__':
    app.run_server(debug=True)
