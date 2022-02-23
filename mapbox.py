import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.express as px
from dash.dependencies import Output, Input
from urllib.request import urlopen
import json
url =  "https://planes-data.s3.amazonaws.com/new_data.json"

def load_http():
    response = urlopen(url)
    data_json = json.loads(response.read())
    longitude = []
    latitude = []

    for i in range(0, len(data_json)):
        latitude.append(data_json[i]['latitude'])
        longitude.append(data_json[i]['longitude'])

    for i in range(0, len(data_json)):
        if float(data_json[i]['longitude']) > 14 and float(data_json[i]['longitude']) < 19.03:
            if float(data_json[i]['latitude']) < (- 0.47 * float(data_json[i]['longitude']) + 58.33): #Czechy
                latitude.remove(data_json[i]['latitude'])
                longitude.remove(data_json[i]['longitude'])

    return longitude, latitude


token = "pk.eyJ1IjoiYnJvb2tlbXllcnMiLCJhIjoiY2tsamtiZ3l0MW55YjJvb2lsbmNxaWo0dCJ9.9iOO0aFkAy0TAP_qjtSE-A"
app = dash.Dash()

temp_lat = []
temp_lon = []
df = pd.read_json(url)
for ind in df.index:
    temp_lat.append(df['latitude'][ind])
    temp_lon.append(df['longitude'][ind])

for ind in df.index:
    if df['longitude'][ind] > 14 and df['longitude'][ind] < 19.03:
        if df['latitude'][ind] < ( - 0.47 * df['longitude'][ind] + 58.33): #Czechy
            print(df['longitude'][ind], df['latitude'][ind])
            temp_lat.remove(df['latitude'][ind])
            temp_lon.remove(df['longitude'][ind])

new_df = {
    "latitude": temp_lat,
    "longitude": temp_lon
}

px.set_mapbox_access_token(token)
fig = px.scatter_mapbox(new_df, lat='latitude', lon='longitude', height=800, width=1024, zoom=5.2)
fig.update_layout(mapbox_style='mapbox://styles/brookemyers/cklk04z7x1f5d17pedafupa3e')
fig.update_traces(mode='markers', marker_color='red', marker_size=10)

app.layout = html.Div(children=[
    html.H1(children='Samoloty przelatujące nad Polską'),

    html.Div(children='''
        Maria Bąk, Piotr Bejenka, Kamil Rubach
    '''),

    dcc.Graph(
        id='live-update-graph',
        figure=fig
    ),

    dcc.Interval(
        id='interval-component', 
        interval=60*1000,
        n_intervals=0
    )
])

@app.callback(Output('live-update-graph', 'figure'), Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    lon, lat = load_http()
   # print(lat[5], lon[5])
    fig.update(data=dict(lat=lat, lon=lon))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)