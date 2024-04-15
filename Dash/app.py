# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.FLATLY]
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


# dummy data of bus route(based on first 500 bus data)
bus_stop = pd.read_csv("route.csv")
items = bus_stop['ServiceNo'].unique().tolist()  # dummy dropdown_busnumber


# dummy df for co2 and assumption
dummy_for_bar = pd.read_csv("bar.csv")
dummy_for_bar['YEAR_MONTH'].astype(str)


# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div('''Reducing CO2 Emissions in Singapore's Public Bus Network''',
                 className="text-primary text-center fs-4", style={'padding-top': '15px'})
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Row([html.Div("Select Bus number:"), 
                    dcc.Dropdown(id='dropdown_1',
                    options=items,
                    value='10',  # default value
                    style={'height': '40px', 'width': '150px'})
            ], style={'padding-left': '80px'}),
            dbc.Row([
                dcc.Graph(id='Singapore_map')
            ], style={"height": "60vh"})
        ], width=6),

        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.P(id='co2-title',
                               children='CO2 Reduction',
                               className='font-weight-bold'),
                        dcc.Graph(id='co2_bar')
                    ])
                ]),
                dbc.Col([
                    html.Div([
                        html.P(id='passenger-title',
                               children='Passenger Volume',
                               className='font-weight-bold'),
                        dcc.Graph(id='passenger_bar')
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
                    html.Div([
                        html.P(id='assumption-title',
                               children='Assumption',
                               className='font-weight-bold text-center')
                               ]),
                dbc.Col(dcc.Graph(id='assumption_bar')),                                 
                dbc.Col(dbc.Card(id="card_assumption", color="success"), style ={'margin-top': '30px'})
            ], style={"height": "40vh",
                      'margin-top': '20px',
                      'margin-left': '8px',
                      'margin-bottom': '20px',
                      'margin-right': '8px'})
        ], width=6),
    ]),

], fluid=True)

# Add controls to build the interaction; https://stackoverflow.com/questions/71920570/how-to-connect-multiple-outputs-to-callbacks


@callback(
    [
        Output(component_id='Singapore_map', component_property='figure'),
        Output(component_id='co2_bar', component_property='figure'),
        Output(component_id='passenger_bar', component_property='figure'),
        Output(component_id='assumption_bar', component_property='figure'),
        Output(component_id='card_assumption', component_property='children')
    ],
    Input(component_id='dropdown_1', component_property='value')
)
def update_graph(col_chosen):

    # 0. filter data by chosen busnumber from dropdown
    # 0-1. update bus route's lat, long, and all passenger taps
    df = bus_stop.loc[bus_stop['ServiceNo'] == col_chosen]
    # 0-2. update data for bar chart
    df_bar = dummy_for_bar.loc[dummy_for_bar['ServiceNo'] == col_chosen]
    # 0-2a. update data for assumption chart
    sum_of_3m = df_bar[['co2_by_car', 'co2_by_bus']].sum()
    sum_df = pd.DataFrame(
        {'Vehicle_type': sum_of_3m.index, 'Sum': sum_of_3m.values})
    sum_df.loc[sum_df['Vehicle_type'] == 'co2_by_car',
               'Vehicle_type'] = 'Private Car'  # rename for label
    sum_df.loc[sum_df['Vehicle_type'] == 'co2_by_bus',
               'Vehicle_type'] = 'Electric bus'  # rename for label
    # text for assumption card
    co2_by_bus = sum_df.iloc[1, 1]
    co2_by_car = sum_df.iloc[0, 1]
    total_saved = co2_by_car - co2_by_bus

    # 1. draw chosen bus route
    px.set_mapbox_access_token(
        open("mapbox_token.py").read())  # public access token
    fig_route = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="all_taps", size="all_taps",
                                  labels={'all_taps':'Passenger volume'},
                                  size_max=15, zoom=11, height=540)

    fig_route.add_traces(px.line_mapbox(
        df, lat="Latitude", lon="Longitude").data)

    # 2. bar chart update
    # 2-1 co2 emission reduction bar_chart
    fig_c = px.bar(df_bar, x="YEAR_MONTH", y="co2_reduction",
                   labels={'YEAR_MONTH': 'Month',
                           'co2_reduction': "CO2 emission reduction"},
                   width=320, height=260)
    fig_c.update_layout(font_size=10, margin=dict(t=30, b=10, l=10, r=10))
    fig_c.update_traces(marker_color='green')

    # 2-2 passenger volume bar chart
    fig_p = px.bar(df_bar, x="YEAR_MONTH", y="passenger_volume",
                   labels={'YEAR_MONTH': 'Month',
                           'passenger_volume': "Passenger volume"},
                   width=320, height=260)
    fig_p.update_layout(font_size=10, margin=dict(t=30, b=10, l=10, r=10))

    # 2-3 assumption bar chart
    fig_a = px.bar(sum_df, x="Vehicle_type", y="Sum",
                   labels={'Vehicle_type': 'Vehicle type',
                           'Sum': "Total CO2 emission"},
                   width=320, height=260)
    fig_a.update_layout(font_size=10, margin=dict(
        t=30, b=10, l=10, r=10), yaxis_type="log")
    fig_a.update_traces(marker_color='orange')

    # 2-4 card of assumption statistics
    card = dbc.Card(
        dbc.CardBody(
            [
                html.P(
                    "Total CO2 emissions by the bus:  " +
                    '{:>12,.0f}'.format(co2_by_bus) + " kg",
                    className="card-text",
                ),
                html.P(
                    "Total CO2 emissions by private car:  " +
                    '{:>12,.0f}'.format(co2_by_car) + " kg",
                    className="card-text",
                ),
                html.P(
                    "Total Saved CO2 emission by using the bus:  " +
                    '{:>12,.0f}'.format(total_saved) + "kg",
                    className="card-text",
                ),
            ],
        ),
    )

    return fig_route, fig_c, fig_p, fig_a, card


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
