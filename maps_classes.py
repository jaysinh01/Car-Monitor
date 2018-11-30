import urllib.request
import simplejson
''' Frequent imports'''
import json
import re
import geocoder
import geopy.geocoders

class nearby:

  # Input whether you want IP address to be asked for
  def __init__(self, destination=None):
    self.destination = destination
    self.API_key = "AI__zaSyCT4l0QIAEcuZbM9M2ZnciH7Cq8M3jQ_nw"
    self.IP_key = "_7cbe04f612f94a95d2eb28f12fd1f40"
    if self.destination is None:
      ip_adress = urllib.request.urlopen("http://whatismyip.org").read()
      url_ip = "http://api.ipstack.com/" + ip_adress + "?access_key=" + self.IP_key
      ip_information =  urllib.request.urlopen(url_ip).read()
      json_object = simplejson.loads(ip_information)
      lat = json_object["latitude"]
      lng = json_object["longitude"]
    else:
      #grab json object from google_maps_v1
      lat = json_object["routes"][0]["legs"][0]["end_location"][0]["lat"]
      lng = json_object["routes"][0]["legs"][0]["end_location"][0]["lng"]
    self.common_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?" \
                      "location=" + lat + "," + lng + "&radius=9000" + "&type="


    # g = geocoder.ip('me')
    # print(g.latlng)

  def common_step(self, desire):
    url = self.common_url + desire + "&key=" + self.API_key
    response = urllib.request.urlopen(url).read()
    json_file = simplejson.loads(response)
    names = ["sorted by Kms"]
    self.place_id = {}
    for row in json_file["results"]:
      # https://developers.google.com/places/web-service/search#nearby-search-and-text-search-responses
      names.append(row["name"])
      self.place_id[row["name"]] = row["id"]
    return names

  def get_shopping_mall(self):
    desire = "shopping_mall"
    self.common_step(desire)

  def get_restaurant(self):
    desire = "restaurant"
    self.common_step(desire)

  def get_gas_station(self):
    desire = "gas_station"
    self.common_step(desire)

  def get_hospital(self):
    desire = "hospital"
    self.common_step(desire)

  def get_parking(self):
    desire = "parking"
    self.common_step(desire)



