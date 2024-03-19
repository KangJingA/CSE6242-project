# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.FLATLY]
app = Dash(__name__, external_stylesheets=external_stylesheets)

path = "C:\\Gatech_OMSA\\2024_Spring\\CSE6242\\Project\\Code\\"
# dummy data # 
items = [3,4,5,6,7] # dummy dropdown
days = ["WEEKDAYS","WEENKEND/HOLIDAYS"] # dummy dropdown
dummy_vol = pd.read_csv("C:\\Gatech_OMSA\\2024_Spring\\CSE6242\\Project\\Code\\dummy_vol.csv")
selected = dummy_vol.query("DAY_TYPE == 'WEEKDAY' and BUS_NUMBER == 4")

dummy_co2 = pd.read_csv("C:\\Gatech_OMSA\\2024_Spring\\CSE6242\\Project\\Code\\co2_dummy.csv")
selected2 = dummy_co2.query("DAY_TYPE == 'WEEKDAY' and BUS_NUMBER == 4")

bus_stop = pd.read_csv("C:\\Gatech_OMSA\\2024_Spring\\CSE6242\\Project\\Code\\BUS_stop_dummy.csv")

# Chart (Temporary)
## Singapore map + busstop
px.set_mapbox_access_token(open("C:\\Gatech_OMSA\\2024_Spring\\CSE6242\\Project\\Code\\mapbox_token.py").read())  # public access token
fig = px.scatter_mapbox(bus_stop, lat="Latitude", lon="Longitude", color="co2_reduction", size="avg_passenger_vol",
                  color_continuous_scale="Viridis", size_max=15, zoom=10, width = 700, height =480)

## bar chart 1
fig_p = px.bar(selected, x="TIME_PER_HOUR", y="TOTAL_PASSENGER_VOL",
               title="Passenger volume", 
               labels={'TIME_PER_HOUR':'Hour', 'TOTAL_PASSENGER_VOL':"Passenger volume(person)"},
               width=400, height=320)
## bar chart 2
fig_c = px.bar(selected2, x="TIME_PER_HOUR", y="co2_reduction",
               title="CO2 emission reduction", 
               labels={'TIME_PER_HOUR':'Hour', 'co2_reduction':"CO2 emission reduction"},
               width=400, height=320)



# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div('test layout', className="text-primary text-center fs-3")
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Row([dcc.Dropdown(id='dropdown_1',
                    options=items,
                    value = 3)
                    ]),
            dbc.Row([dcc.Graph(figure=fig , id='Singapore_map')])         
        ], width=6),

        dbc.Col([
            dbc.Row([dcc.Dropdown(id='dropdown_2',
                    options=days,
                    value = "WEEKDAYS")
                    ])
            dbc.Row([dcc.Graph(figure=fig_c , id='co2_chart')]),
            dbc.Row([dcc.Graph(figure=fig_p , id='passenger_chart')])
          
        ], width=6),
    ]),

], fluid=True)

# Add controls to build the interaction- not available
#@callback(
#    Output(component_id='my-first-graph-final', component_property='figure'),
#    Input(component_id='dropdown_1', component_property='value')
#)
#def update_graph(col_chosen):
#    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
#    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)