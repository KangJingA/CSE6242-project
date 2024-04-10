from buses import LTA
import csv
apiKey:str = "75cstockTLWN9wEcc9RE6Q=="

lta = LTA(apiKey)

# retrieves bus stops and saves them in a csv
max_lines = 10000
csv_file_path = "bus_routes.csv"
write_headers = False
with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    for i in range(0, max_lines, 500):
        response = lta.get_bus_routes(i)
        bus_routes = response['value']
        
        header = bus_routes[0].keys()
        
        if not write_headers:
            csv_writer.writerow(header)
            write_headers = True
            
        for bus_route in bus_routes: 
            csv_writer.writerow(bus_route.values())
    
    print("csv download complete")