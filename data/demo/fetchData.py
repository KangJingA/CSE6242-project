from buses import LTA
import csv
apiKey:str = "75cstockTLWN9wEcc9RE6Q=="

lta = LTA(apiKey)

# retrieves all bus routes and saves them in a csv
csv_file_path = "bus_routes.csv"
write_headers = False
with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    skip = 0
    while True:
        response = lta.get_bus_routes(skip)
        
        bus_routes = response['value']
        
        if len(bus_routes) == 0:
            break
        
        header = bus_routes[0].keys()
        
        if not write_headers:
            csv_writer.writerow(header)
            write_headers = True
            
        for bus_route in bus_routes: 
            csv_writer.writerow(bus_route.values())
        
        print("written " + str(skip + 500) + "lines")
        skip += 500
    
    print("csv download complete with total of " + str(skip + 500) + "lines")
    
    
csv_file_path = "bus_stops.csv"
write_headers = False
with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    skip = 0
    while True:
        response = lta.get_bus_stops2(skip)
        
        bus_stops = response['value']
        
        if len(bus_stops) == 0:
            break
        
        header = bus_stops[0].keys()
        
        if not write_headers:
            csv_writer.writerow(header)
            write_headers = True
            
        for bus_route in bus_stops: 
            csv_writer.writerow(bus_route.values())
        
        print("written " + str(skip + 500) + "lines")
        skip += 500
    
    print("csv download complete with total of " + str(skip + 500) + "lines")