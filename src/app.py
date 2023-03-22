import pandas as pd
from dash import dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import altair as alt

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

data = pd.read_csv('data/van_house.csv')

def plot_bar(xmax):
    chart = alt.Chart(
        data[data['current_land_value'] < xmax]
    ).mark_bar().encode(
        x=alt.X("current_land_value", title="Price"),
        y=alt.Y("zoning_classification", title="Zoning Type"),
        color='zoning_classification',
        tooltip='current_land_value'
    ).properties(
        title="Price by Zoning Type"
    )
    return chart.to_html()

app.layout = html.Div([
        html.Iframe(
            id='bar',
            srcDoc=plot_bar(xmax=2500000),
            style={'border-width': '0', 'width': '100%', 'height': '400px'}),
        dcc.Slider(id='xslider', min=0, max=5000000, value=2500000,)
])

@app.callback(
    Output('bar', 'srcDoc'),
    Input('xslider', 'value')
)

def update_output(xmax):
    return plot_bar(xmax)

if __name__ == '__main__':
    app.run_server(debug=True)
