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


def plot_density(xmax):
    density = alt.Chart(
        data[data['current_land_value'] < xmax],
        title='Price by Area'
    ).transform_density(
        'current_land_value',
        groupby=['Geo Local Area'],
        as_=['current_land_value', 'density'],
    ).mark_area(
        opacity=0.6
    ).encode(
        x=alt.X('current_land_value',title='Price'),
        y='density:Q',
        color='Geo Local Area'
    )
    return density.to_html()


app.layout = html.Div([
        html.H1('Vancouver Housing Price'),
        dcc.Slider(id='xslider', min=0, max=5000000, value=2500000),
        html.Iframe(
            id='density',
            srcDoc=plot_density(xmax=2500000),
            style={'border-width': '0', 'width': '100%', 'height': '400px'}
        ),
        html.Iframe(
            id='bar',
            srcDoc=plot_bar(xmax=2500000),
            style={'border-width': '0', 'width': '100%', 'height': '400px'}
        )
])

@app.callback(
    Output('bar', 'srcDoc'),
    Output('density', 'srcDoc'),
    Input('xslider', 'value')
)

def update_output(xmax):
    return plot_bar(xmax), plot_density(xmax)

if __name__ == '__main__':
    app.run_server(debug=True)
