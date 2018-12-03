import urllib.request
import simplejson
from maps_classes import NearBy
import os.path
''' Frequent imports'''
import json
import re
# import geocoder
# import geopy.geocoders



class Directions:

  def __init__(self, address_destination, address_origin=None):
    self.API_key = ""
    self.freq_url = "https://maps.googleapis.com/maps/api/directions/json?"
    self.address_destination = address_destination
    self.address_origin = address_origin
    if address_origin is None:
      self.coordinates = NearBy.current_location()
      # potential function to look up place id
      dummy_json_url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(self.coordinates[0]) + \
      "," + str(self.coordinates[1]) + "&key=" + self.API_key
      dummy_json = urllib.request.urlopen(dummy_json_url).read()
      dummy_json = simplejson.loads(dummy_json)
      self.origin = dummy_json["results"][0]["formatted_address"].lower()
    else:
        self.origin = address_origin
    self.file_name = self.origin + self.address_destination + ".json"
    file_check = os.path.isfile(self.file_name)
    if file_check:
      self.cFlag = True
    else:
      self.cFlag = False
    with open("history.txt", "a+") as history:
      history.write(self.origin.replace("+", " ") + "\n")
      history.write(address_destination.replace("+", " ") + "\n")

    with open("history.txt", "a+") as history:
        history.write(address_origin.replace("+", " ") + "\n")
        history.write(address_destination.replace("+", " ") + "\n")
    pass

  def json_object(self):
    if self.cFlag:
      with open(self.file_name) as file_stream:
        json_string = json.load(file_stream)
    else:
      json_string = self.grab_online_json()
    return json_string


  def grab_online_json(self):
    try:
        url = self.freq_url + "origin=" + self.origin + "destination=" + self.address_destination + "key=" + self.API_key
    except:
        url = self.freq_url + "origin=" + self.origin + "destination=" + "place_id:" + self.address_destination\
            + "key=" + self.API_key
    response = urllib.request.urlopen(url).read()
    json_object = simplejson.loads(response)
    with open(self.file_name, "w") as result:
        simplejson.dump(json_object, result)
    return json_object

  def get_directions(self, json_file):
    total_time = 0
    total_distance = 0
    final_details = {}
    for row in json_file["routes"][0]["legs"][0]["steps"]:
      direction = row['html_instructions']
      distance = row['distance']['text']
      duration = row['duration']['text']
      time = re.findall("\d+", duration)
      total_time += int(time[0])
      # https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string
      length_of_road = re.findall("\d+\.\d+", distance)
      total_distance += float(length_of_road[0])
      html_tags = re.findall("<[^<]+?>", direction)
      i = 0
      for remove in html_tags:
        direction = direction.replace(remove, "")
        final_details["directions"][i] = direction + " in " + distance + " in about " + duration
        i += 1
    final_details["distance"] = "The total distance is " + str(total_distance) + " km"
    final_details["duration"] = "The total duration is " + str(total_time) + " mins"
    return final_details

def check_place(country, city, address, state=None):
  try:
    api_key = "AIzaSyCT4l0QIAEcuZbM9M2ZnciH7Cq8M3jQ_nw"
    if state is None:
      url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + address + country + city + "key=" + api_key
    check_place_object = urllib.request.urlopen(url).read()
    check_place_object = simplejson.loads(check_place_object)
    address = check_place_object["results"][0]["formatted_address"]
    return address
  except:
    return None


"""
Features:

- give suggested adresses
- give direction based on place id or an address (make a different function)
- give lat and ln of the destination
- if partial match is true present json_object["geocoded_waypoints"][0]["place_id"]
 json_object["geocoded_waypoints"][1]["place_id"]
 
https://maps.googleapis.com/maps/api/geocode/json?place_id=ChIJd8BlQ2BZwokRAFUEcm_qrcA&key=YOUR_API_KEY
"""
