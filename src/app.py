from dash import dash, html

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

app.layout = html.Div([
    html.H1('Hi Ken'),
    html.Iframe(
        srcDoc=chart.plot_density(),
        style={'border-width': '0', 'width': '100%', 'height': '400px'}
    ),
    html.Iframe(
        srcDoc=chart.plot_bar(),
        style={'border-width': '0', 'width': '100%', 'height': '400px'}
    )
])

def plot_bar():
    return alt.Chart(data).mark_bar().encode(
        x=alt.X("current_land_value", title="Price"),
        y=alt.Y("zoning_classification", title="Zoning Type"),
        color='zoning_classification',
        tooltip='current_land_value'
    ).properties(
        title="Price by Zoning Type"
    ).to_html()


def plot_density():    
    return alt.Chart(data, title='Price by Area').transform_density(
        'current_land_value',
        groupby=['Geo Local Area'],
        as_=['current_land_value', 'density'],
    ).mark_area(
        opacity=0.6
    ).encode(
        x=alt.X('current_land_value',title='Price'),
        y='density:Q',
        color='Geo Local Area'
    ).to_html()


if __name__ == '__main__':
    app.run_server(debug=True)
