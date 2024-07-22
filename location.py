from geopy import Photon
from geopy.geocoders import Nominatim


import certifi
import ssl
import geopy.geocoders
ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx


class Location:
    data_adress = {}

    def get_address(self, cordinates):
        locator = Nominatim(user_agent="measurements")
        coordinates = cordinates[0], cordinates[1]
        location = locator.reverse(coordinates)
        address_data = location.raw

        return address_data

    def save_data(self, cordinates):
        Location.data_adress = self.get_address(cordinates)
        # print(Location.data_adress['display_name'])

    def get_spec_add(self, name):
        return Location.data_adress["address"][name]