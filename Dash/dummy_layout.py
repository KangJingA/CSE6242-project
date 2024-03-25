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
dummy_vol = pd.read_csv("dummy_vol.csv")
selected = dummy_vol.query("DAY_TYPE == 'WEEKDAY' and BUS_NUMBER == 4")

dummy_co2 = pd.read_csv("co2_dummy.csv")
selected2 = dummy_co2.query("DAY_TYPE == 'WEEKDAY' and BUS_NUMBER == 4")

bus_stop = pd.read_csv("dummy_for_route.csv")
assumption = [{'Vehicle type':'Bus','CO2 emission': 1500},{'Vehicle type':'Private car','CO2 emission': 4500}]
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
fig_c = px.bar(selected2, x="TIME_PER_HOUR", y="co2_reduction",
               labels={'TIME_PER_HOUR':'month', 'co2_reduction':"CO2 emission reduction"},
               width=320, height=260)
fig_c.update_layout(font_size=10, margin=dict(t=30, b=10, l=10, r=10))
fig_c.update_traces(marker_color='green')


## bar chart 2
fig_p = px.bar(selected, x="TIME_PER_HOUR", y="TOTAL_PASSENGER_VOL",
               labels={'TIME_PER_HOUR':'month', 'TOTAL_PASSENGER_VOL':"Passenger volume(person)"},
                width=320, height=260)
fig_p.update_layout(font_size=10, margin=dict(t=30, b=10, l=10, r=10))


## bar chart 3 - Assumption bar chart
fig_a = px.bar(assumption, x="Vehicle type", y="CO2 emission",
               labels={'Vehicle type':'Vehicle_type', 'CO2 emission':"Total CO2 emission"},
               width=320, height=260)
fig_a.update_layout(font_size=10, margin=dict(t=30, b=10, l=10, r=10))
fig_a.update_traces(marker_color='red')


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
                        ])
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
                dbc.Col([html.Div('Total saved CO2 emission: 3000')]) 
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
