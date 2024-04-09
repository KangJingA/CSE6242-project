import numpy as np
import pandas as pd
import os
from data.buses import LTA

# Preprocess df_bus_route to get origin-destination distances for each bus no.
def preprocess_df_bus_route_1d(df_bus_route):
    """
    Direction == 1
    """
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


def preprocess_df_bus_route_2d(df_bus_route):
    """
    (Direction == 1) & (Direction == 2)
    """
    # Input
    df = df_bus_route

    # Get ServiceNo with two directions
    service_no_with_two_directions = df.groupby('ServiceNo')['Direction'].max()
    service_no_with_two_directions = service_no_with_two_directions[service_no_with_two_directions == 2].index

    # Filter the original DataFrame to include only ServiceNo with two directions
    df = df[df['ServiceNo'].isin(service_no_with_two_directions)]

    # Filter to include only Direction == 1 for each unique ServiceNo
    df1 = df[df['Direction'] == 1]
    df2 = df[df['Direction'] == 2]  

    def process_df_by_serviceNo(df):
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
        df_bus_route_processed['Direction'] = df['Direction'].unique()[0]

        # Reset index to make ServiceNo a column instead of index
        df_bus_route_processed.reset_index(inplace=True)

        # Reorder columns
        df_bus_route_processed = df_bus_route_processed[['ServiceNo', 'Direction', 'origin_bus_stop', 'dest_bus_stop', 'origin_dest_distance']]
        return df_bus_route_processed

    df1_processed = process_df_by_serviceNo(df1)
    df2_processed = process_df_by_serviceNo(df2)

    # Concatenate the two DataFrames
    concatenated_df = pd.concat([df1_processed, df2_processed])

    # Sort the concatenated DataFrame by ServiceNo and Direction
    sorted_df = concatenated_df.sort_values(by=['ServiceNo', 'Direction'])

    # Reset the index
    sorted_df.reset_index(drop=True, inplace=True)

    # Convert origin_bus_stop and dest_bus_stop to integers
    sorted_df['origin_bus_stop'] = sorted_df['origin_bus_stop'].astype(int)
    sorted_df['dest_bus_stop'] = sorted_df['dest_bus_stop'].astype(int)
    return sorted_df

# Preprocess total-trips df to get monthly origin-dest total trips
def preprocess_totalTrips_df(df):
    # Filter 'PT_TYPE' == 'BUS'
    df = df[df['PT_TYPE'] == 'BUS']

    # Group by YEAR_MONTH, ORIGIN_PT_CODE, DESTINATION_PT_CODE and sum TOTAL_TRIPS
    condensed_df = df.groupby(['YEAR_MONTH', 'ORIGIN_PT_CODE', 'DESTINATION_PT_CODE']).agg({'TOTAL_TRIPS': 'sum'}).reset_index()
    return condensed_df

# Merge df_total_trips into df_2d
def merge_distance_totalTrips(df_2d, df_total_trips):
    """
    Input
        - df_2d can be df_1d as well
    """
    merged_df = df_2d.merge(df_total_trips, 
                                left_on=['origin_bus_stop', 'dest_bus_stop'], 
                                right_on=['ORIGIN_PT_CODE', 'DESTINATION_PT_CODE'], 
                                how='left')
    return merged_df

# Preprocess df_taps
def preprocess_df_taps(df_taps):
    df = df_taps

    # Filter 'PT_TYPE' == 'BUS'
    df = df[df['PT_TYPE'] == 'BUS']

    # Group by YEAR_MONTH, PT_CODE, and sum TOTAL_TAP_IN_VOLUME TOTAL_TAP_OUT_VOLUME
    condensed_df = df.groupby(['YEAR_MONTH', 'PT_CODE']).agg({'TOTAL_TAP_IN_VOLUME': 'sum', 'TOTAL_TAP_OUT_VOLUME': 'sum'}).reset_index()
    condensed_df['TOTAL_TAP_VOLUME'] = condensed_df['TOTAL_TAP_IN_VOLUME'] + condensed_df['TOTAL_TAP_OUT_VOLUME']
    return condensed_df

# Merge df_taps in df_distance_totalTrips
def merge_taps_distance_totalTrips(df_taps, df_distance_totalTrips):
    # Merge the dataframes based on matching YEAR_MONTH and PT_CODE
    merged_df = df_distance_totalTrips.merge(df_taps, 
                                            left_on=['YEAR_MONTH', 'ORIGIN_PT_CODE'], 
                                            right_on=['YEAR_MONTH', 'PT_CODE'], 
                                            how='left')

    # Merge again for the destination PT_CODE
    merged_df = merged_df.merge(df_taps, 
                                left_on=['YEAR_MONTH', 'DESTINATION_PT_CODE'], 
                                right_on=['YEAR_MONTH', 'PT_CODE'], 
                                suffixes=('_origin', '_destination'), 
                                how='left')

    # Calculate the passenger volume by summing TOTAL_TAP_VOLUME from both origin and destination
    merged_df['passenger_volume'] = merged_df['TOTAL_TAP_VOLUME_origin'] + merged_df['TOTAL_TAP_VOLUME_destination']

    # Calculate the passenger volume by summing TOTAL_TAP_VOLUME from both origin and destination
    merged_df['passenger_volume'] = merged_df['TOTAL_TAP_VOLUME_origin'] + merged_df['TOTAL_TAP_VOLUME_destination']

    # Drop unnecessary columns
    merged_df.drop(columns=['PT_CODE_origin', 'TOTAL_TAP_IN_VOLUME_origin', 'TOTAL_TAP_OUT_VOLUME_origin',  'PT_CODE_destination',
                            'TOTAL_TAP_IN_VOLUME_destination', 'TOTAL_TAP_OUT_VOLUME_destination', 'ORIGIN_PT_CODE', 'DESTINATION_PT_CODE'], inplace=True)
    return merged_df

# Compute bus/car CO2 emission
def get_df_co2(df_taps_distance_totalTrips):
    df = df_taps_distance_totalTrips
    bus_CO2_rate = 0.48  # kg/km
    car_CO2_rate = 0.167  # kg/km
    bus2car_ratio = 1/4  # approximation: 1/4 passengers taking car and carpool
    df['co2_by_bus'] = df['origin_dest_distance']*df['TOTAL_TRIPS']*bus_CO2_rate
    df['co2_by_car'] = df['origin_dest_distance']*df['TOTAL_TRIPS']*df['passenger_volume']*bus2car_ratio*car_CO2_rate
    df['co2_reduction'] = df['co2_by_car'] - df['co2_by_bus']
    return df