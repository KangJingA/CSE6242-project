# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go




# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.FLATLY]
app = Dash(__name__, external_stylesheets=external_stylesheets)


# dummy data # 
items = [10,3,4,5,6,7] # dummy dropdown_busnumber
dummy_vol =  [{'YEAR_MONTH':'2023.10','Passenger_volume': 2400},{'YEAR_MONTH':'2023.11','Passenger_volume': 3200},{'YEAR_MONTH':'2023.12','Passenger_volume': 2100}]
dummy_vol = pd.DataFrame.from_dict(dummy_vol)

dummy_co2 = [{'YEAR_MONTH':'2023.10','CO2_reduction': 1200},{'YEAR_MONTH':'2023.11','CO2_reduction': 1600},{'YEAR_MONTH':'2023.12','CO2_reduction': 1100}]
dummy_co2 = pd.DataFrame.from_dict(dummy_co2)

bus_stop = pd.read_csv("dummy_for_route.csv")
assumption = [{'Vehicle_type':'Bus','CO2_emission': 1500},{'Vehicle_type':'Private car','CO2_emission': 4500}]
assumption = pd.DataFrame.from_dict(assumption)

# Chart (Temporary)
## Singapore map + busstop dummy
px.set_mapbox_access_token(open("mapbox_token.py").read())  # public access token

# draw bus route

fig_route = px.scatter_mapbox(bus_stop, lat="Latitude", lon="Longitude", color = "all_taps", size = "all_taps",
                 size_max=15, zoom=11, height =540)
route = list(range(len(bus_stop))) # dummy route of selected bus 10; row number value
fig_route.add_traces(px.line_mapbox(bus_stop.loc[route], lat="Latitude", lon="Longitude").data)




## bar chart 1
fig_c = px.bar(dummy_co2, x="YEAR_MONTH", y="CO2_reduction",
               labels={'YEAR_MONTH':'Month', 'CO2_reduction':"CO2 emission reduction"},
               width=320, height=260)
fig_c.update_layout(font_size=10, margin=dict(t=30, b=10, l=10, r=10))
fig_c.update_traces(marker_color='green')


## bar chart 2
fig_p = px.bar(dummy_vol, x="YEAR_MONTH", y="Passenger_volume",
               labels={'YEAR_MONTH':'Month', 'Passenger_volume':"Passenger volume"},
                width=320, height=260)
fig_p.update_layout(font_size=10, margin=dict(t=30, b=10, l=10, r=10))


## bar chart 3 - Assumption bar chart
fig_a = px.bar(assumption, x="Vehicle_type", y="CO2_emission",
               labels={'Vehicle_type':'Vehicle type', 'CO2_emission':"Total CO2 emission"},
               width=320, height=260)
fig_a.update_layout(font_size=10, margin=dict(t=30, b=10, l=10, r=10))
fig_a.update_traces(marker_color='orange')

## card for assumption
card =  dbc.Card(
    dbc.CardBody(
        [
           html.P(
                "Total C02 emissions by the bus: 1,500 kg/km",
                className="card-text",
            ),
            html.P(
                "Total C02 emissions by private car: 4,500 kg/km",
                className="card-text",
            ),
            html.P(
                "Total Saved: 3,000 kg/km",
                className="card-text",
            ),
        ],
    ),
)



# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div('test layout', className="text-primary text-center fs-3")
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Row([dcc.Dropdown(id='dropdown_1',
                    options=items,
                    value = "select bus number",
                    style={'height': '40px', 'width': '150px'})
                    ]),
            dbc.Row([
                dcc.Graph(figure=fig_route , id='Singapore_map')
                ],style={"height": "60vh"})         
        ], width=6),

        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.P(id='co2-title',
                               children='CO2 Reduction',
                               className='font-weight-bold'),
                        dcc.Graph(figure=fig_c , id='co2_chart')
                            ])
                        ]),
                dbc.Col([
                    html.Div([
                        html.P(id='passenger-title',
                               children='Passenger Volume',
                               className='font-weight-bold'),
                        dcc.Graph(figure=fig_p , id='passenger_chart')                                          
                        ])
                        ], style={'margin-top': '8px', 
                           'margin-left': '8px',
                           'margin-bottom': '16px', 
                           'margin-right': '8px'})
                    ],
                    style={"height": "40vh",
                           'margin-top': '8px', 
                           'margin-left': '8px',
                           'margin-bottom': '16px', 
                           'margin-right': '8px'}
                    ),
            dbc.Row([
                dbc.Col([
                    html.Div([
                            html.P(id='assumption-title',
                                   children='Assumption',
                                   className='font-weight-bold'),
                            dcc.Graph(figure=fig_a , id='assumption_chart'),
                            ])
                        ]),
                dbc.Col(dbc.Card(card, color="success")) 
                    ], style={"height": "20vh"})                  
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
