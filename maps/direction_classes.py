import urllib.request
import simplejson
from maps_classes import NearBy
import os.path
''' Frequent imports'''
import json
import re



class Directions:

    def __init__(self, address_destination, address_origin=None):
        self.API_key = "AIzaSyCT4l0QIAEcuZbM9M2ZnciH7Cq8M3jQ_nw"
        self.freq_url = "https://maps.googleapis.com/maps/api/directions/json?"
        # address passed with " " replaced with "+"
        self.address_destination = address_destination
        self.address_origin = address_origin
        # if origin is not provided then call Nearby class and get the current location
        if address_origin is None:
            # get the coordinates of the current location by using Nearby class
            class_initiation = NearBy()
            self.coordinates = class_initiation.current_location()
            # potential function to look up place id
            # The following block of code will extract street address and replace coordinates
            print(self.coordinates)
            dummy_json_url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(self.coordinates[0]) + \
            "," + str(self.coordinates[1]) + "&key=" + self.API_key
            dummy_json = urllib.request.urlopen(dummy_json_url).read()
            dummy_json = simplejson.loads(dummy_json)
            self.origin = dummy_json["results"][0]["formatted_address"].lower()
            print(self.origin)
        else:
            self.origin = address_origin
        self.file_name = self.origin + self.address_destination + ".json"
        # it will check if the address have been previously searched and if it has
        # it will extract result from there
        file_check = os.path.isfile(self.file_name)
        # The following two statements will be used to evaluate different case in the method to handle data
        if file_check:
            self.cFlag = True
        else:
            self.cFlag = False
            # The following will add origin and destination in means of keeping track of history
            with open("history.txt", "a+") as history:
                history.write(self.origin.replace("+", " ") + "\n")
                history.write(self.address_destination.replace("+", " ") + "\n")

    def json_object(self):
        # if the file is found then it will load the json object from the file or else it will call
        # grab_online_json method which will grab the data from the web and store it in a file for future offline use
        if self.cFlag:
            with open(self.file_name) as file_stream:
                json_string = json.load(file_stream)
        else:
            json_string = self.grab_online_json()
        return json_string

    def grab_online_json(self):
        # The try and except will take care if the destination is in terms of street address or a place_id

        url = self.freq_url + "origin=" + str(self.coordinates[0]) + "," + str(self.coordinates[1]) + "&destination="\
              + "place_id:" + self.address_destination + "&key=" + self.API_key
        # The following block of code extract the json file, store it in a file and return the object
        response = urllib.request.urlopen(url).read()
        json_object = simplejson.loads(response)
        with open(self.file_name, "w") as result:
            simplejson.dump(json_object, result)
        return json_object

    def get_directions(self, json_file):
        total_time = 0
        final_details = {}
        final_details["directions"] = []
        # "step" is a list of all the details regarding details of the directions
        for row in json_file["routes"][0]["legs"][0]["steps"]:
            # The key "html_instruction" equates to turns to take written in html
            direction = row['html_instructions']
            # extract the distance and the duration to stay on the same road
            distance = row['distance']['text']
            duration = row['duration']['text']
            # find decimal and floating number from the string so it can be used to tally up the
            # total time and distance
            time = re.findall("\d+", duration)
            total_time += int(time[0])
            # find all the html tags in the sentence
            html_tags = re.findall("<[^<]+?>", direction)
            # The following for loop removes all the HTML text and forms a simple sentence
            road_flag = False
            destination_flag = False
            for remove in html_tags:
                #CHANGEEEE
                direction = direction.replace(remove, "")
            if "Restricted usage road" in direction:
                direction = re.sub("Restricted usage road", " ", direction)
                road_flag = True
            if "Destination will be on the" in direction:
                tag = re.findall("Destination will be on the (right|left)", direction)
                tag = "Destination will be on the " + tag[0]
                direction = re.sub(tag, " ", direction)
                destination_flag = True
            one_step = direction + " in " + distance + " in about " + duration
            final_details["directions"].append(one_step)
            if road_flag is True:
                final_details["directions"].append("Restricted usage road")
            if destination_flag is True:
                final_details["directions"].append(tag)

        total_distance = json_file["routes"][0]["legs"][0]["distance"]["text"]
        # Adds more information such total distance and duration in the dictionary to be returned
        final_details["distance"] = str(total_distance)
        final_details["duration"] = str(total_time) + " minutes"
        return final_details


def check_place(country, city, address):
    try:
        api_key = "AIzaSyCT4l0QIAEcuZbM9M2ZnciH7Cq8M3jQ_nw"
        # Forms a url which will be used to evaluate any given address
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + address + "+" + city + \
              "+" + country + "&key=" + api_key
        # The following block of code will evaluate the given address and give another suggested address
        check_place_object = urllib.request.urlopen(url).read()
        check_place_object = simplejson.loads(check_place_object)
        address = check_place_object["results"][0]["formatted_address"]
        place_id = check_place_object["results"][0]["place_id"]
        return [address, place_id]
    except:
        return [None, None]


"""
  Features:
  
  - give suggested adresses
  - give direction based on place id or an address (make a different function)
  - give lat and ln of the destination
  - if partial match is true present json_object["geocoded_waypoints"][0]["place_id"]
   json_object["geocoded_waypoints"][1]["place_id"]
   
  https://maps.googleapis.com/maps/api/geocode/json?place_id=ChIJd8BlQ2BZwokRAFUEcm_qrcA&key=YOUR_API_KEY
  """
