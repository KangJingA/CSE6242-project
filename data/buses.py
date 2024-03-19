import requests


class LTA(object):

    def __init__(self, apiKey) -> None:
        self.apiKey = apiKey
        self.url = "http://datamall2.mytransport.sg/ltaodataservice/"

    def __get_headers(self):
        return {
            "AccountKey": self.apiKey,
            "accept": "application/json"
        }

    def get_bus_routes(self):
        url = self.url + "BusRoutes"
        response = requests.get(url, headers=self.__get_headers())

        return response.json()

    def get_bus_stops(self):
        url = self.url + "BusStops"
        response = requests.get(url, headers=self.__get_headers())

        return response.json()

    def get_passenger_vol_by_bus_stops(self):
        url = self.url + "PV/Bus"
        response = requests.get(url, headers=self.__get_headers())

        return response.json()
