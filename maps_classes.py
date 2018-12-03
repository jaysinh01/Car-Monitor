import urllib.request
import simplejson
''' Frequent imports'''
import json
import re
# import geocoder
# import geopy.geocoders


class NearBy:

    # Input whether you want IP address to be asked for
    # when this is initialized without any input it will show you nearby results using IP address
    # Please pass json_object created by direction_classes.py
    def __init__(self, destination=None):
        self.destination = destination
        self.API_key = "AIzaSyCT4l0QIAEcuZbM9M2ZnciH7Cq8M3jQ_nw"
        self.IP_key = "7cbe04f612f94a95d2eb28f12fd1f40"
        self.place_id = {}
        self.names = ["sorted by Kms"]
        if self.destination is None:
            ip_address = "75.152.216.81"
            url_ip = "http://api.ipstack.com/" + ip_address + "?access_key=" + self.IP_key
            ip_information = urllib.request.urlopen(url_ip).read()
            json_object = simplejson.loads(ip_information)
            self.lat = json_object["latitude"]
            self.lng = json_object["longitude"]
            """ip_address = urllib.request.urlopen("http://whatismyip.org").read()
              url_ip = "http://api.ipstack.com/" + ip_address + "?access_key=" + self.IP_key
              """

        else:
            # grab json object from google_maps_v1
            self.lat = self.destination["routes"][0]["legs"][0]["end_location"][0]["lat"]
            self.lng = self.destination["routes"][0]["legs"][0]["end_location"][0]["lng"]
            self.common_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?" \
                              "location=" + self.lat + "," + self.lng + "&radius=9000" + "&type="


      # g = geocoder.ip('me')
      # print(g.latlng)

    def common_step(self, desire):
        url = self.common_url + desire + "&key=" + self.API_key
        response = urllib.request.urlopen(url).read()
        json_file = simplejson.loads(response)
        for row in json_file["results"]:
            # https://developers.google.com/places/web-service/search#nearby-search-and-text-search-responses
            self.names.append(row["name"])
            self.place_id[row["name"]] = row["id"]

    def get_shopping_mall(self):
        desire = "shopping_mall"
        self.common_step(desire)
        return self.names

    def get_restaurant(self):
        desire = "restaurant"
        self.common_step(desire)
        return self.names

    def get_gas_station(self):
        desire = "gas_station"
        self.common_step(desire)
        return self.names

    def get_hospital(self):
        desire = "hospital"
        self.common_step(desire)
        return self.names

    def get_parking(self):
        desire = "parking"
        self.common_step(desire)
        return self.names

    def get_place_id(self):
        return self.place_id

    def current_location(self):
        return [self.lat, self.lng]
