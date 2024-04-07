import numpy as np
import pandas as pd
import os
from data.buses import LTA

# Function to preprocess df_bus_route
def preprocess_df_bus_route(df_bus_route):
    # Input
    df = df_bus_route

    # Get ServiceNo with two directions
    service_no_with_two_directions = df.groupby('ServiceNo')['Direction'].max()
    service_no_with_two_directions = service_no_with_two_directions[service_no_with_two_directions == 2].index

    # Filter the original DataFrame to include only ServiceNo with two directions
    df = df[df['ServiceNo'].isin(service_no_with_two_directions)]

    # Filter to include only Direction == 1 for each unique ServiceNo
    df = df[df['Direction'] == 1]

    # Get the bus stop code when StopSequence is 1 for each bus
    origin_bus_stop = df[df['StopSequence'] == 1].groupby('ServiceNo').agg(
        origin_bus_stop=('BusStopCode', 'first')
    )
    # Get the bus stop code when StopSequence is the max for each bus
    destination_bus_stop = df.groupby('ServiceNo').agg(
        dest_bus_stop=('BusStopCode', 'last'),
        origin_dest_distance=('Distance', 'last')
    )

    # Merge origin_bus_stop into destination_bus_stop DataFrame
    df_bus_route_processed = destination_bus_stop.merge(origin_bus_stop, left_index=True, right_index=True, how='left')

    # Add Direction column
    df_bus_route_processed['Direction'] = 1

    # Reset index to make ServiceNo a column instead of index
    df_bus_route_processed.reset_index(inplace=True)

    # Reorder columns
    df_bus_route_processed = df_bus_route_processed[['ServiceNo', 'Direction', 'origin_bus_stop', 'dest_bus_stop', 'origin_dest_distance']]

    return df_bus_route_processed
