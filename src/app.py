import pandas as pd
from dash import dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import altair as alt

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

data = pd.read_csv('../data/van_house.csv')

def plot_bar(xmax, geolist):
    chart = alt.Chart(
        data[
            (data['current_land_value'] < xmax) &
            (data['Geo Local Area'].isin(geolist))
        ]
    ).mark_bar().encode(
        x=alt.X("current_land_value", title="Price"),
        y=alt.Y("zoning_classification", title="Zoning Type"),
        color='zoning_classification',
        tooltip='current_land_value'
    ).properties(
        title="Price by Zoning Type"
    )
    return chart.to_html()


def plot_density(xmax, geolist):
    density = alt.Chart(
        data[
            (data['current_land_value'] < xmax) &
            (data['Geo Local Area'].isin(geolist))
        ]
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
    ).properties(
        title="Price by Location"
    )
    return density.to_html()


app.layout = html.Div([
        html.H1('Vancouver Housing Price'),
        dcc.Slider(id='xslider', min=0, max=5000000, value=2500000),
        dcc.Checklist(
            id='ychecklist',
            options=['Downtown','Fairview','Kitsilano','Mount Pleasant','Renfrew-Collingwood'],
            value=['Downtown']
        ),
        html.Iframe(
            id='density',
            srcDoc=plot_density(xmax=2500000, geolist=['Downtown']),
            style={'border-width': '0', 'width': '100%', 'height': '400px'}
        ),
        html.Iframe(
            id='bar',
            srcDoc=plot_bar(xmax=2500000, geolist=['Downtown']),
            style={'border-width': '0', 'width': '100%', 'height': '400px'}
        )
])

@app.callback(
    Output('bar', 'srcDoc'),
    Output('density', 'srcDoc'),
    Input('xslider', 'value'),
    Input('ychecklist', 'value')
)

def update_output(xmax, geolist):
    return plot_bar(xmax, geolist), plot_density(xmax, geolist)

if __name__ == '__main__':
    app.run_server(debug=True)
