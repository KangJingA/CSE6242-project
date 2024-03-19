from buses import LTA

apiKey:str = "75cstockTLWN9wEcc9RE6Q=="

lta = LTA(apiKey)

print(lta.get_passenger_vol_by_bus_stops())