import urllib.request
import simplejson


class NearBy:

    # Input whether you want IP address to be asked for
    # when this is initialized without any input it will show you nearby results using IP address
    # Please pass json_object created by direction_classes.py
    def __init__(self, destination=None):
        # The destination taken will be taken in a form of json_object created in the direction_classes.py
        self.destination = destination
        self.API_key = "AIzaSyCT4l0QIAEcuZbM9M2ZnciH7Cq8M3jQ_nw"
        self.IP_key = "9cb6419f3c8281af7c0523454efdb0a0"
        self.place_id = {}
        self.names = []
        self.lat = 0
        self.lng = 0
        # If no destination is entered then find location using IP address
        if self.destination is None:
            ip_address = "2620:101:c040:85c:b501:b29b:f0d3:1cb7"
            url_ip = "http://api.ipstack.com/" + ip_address + "?access_key=" + self.IP_key
            ip_information = urllib.request.urlopen(url_ip).read()
            # Take the json response created by calling the website and store it as
            # recursive dict and list and dict and list...
            json_object = simplejson.loads(ip_information)
            # store the value of "latitude" and "longitude" from the json_object dict
            self.lat = json_object["latitude"]
            self.lng = json_object["longitude"]

        else:
            # grabs coordinates from json_object passed in the destination
            self.lat = self.destination["routes"][0]["legs"][0]["end_location"][0]["lat"]
            self.lng = self.destination["routes"][0]["legs"][0]["end_location"][0]["lng"]
        # set up an independent part of the nearby url used to request data
        self.common_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?" \
                          "location=" + str(self.lat) + "," + str(self.lng) + "&radius=9000" + "&type="

    def common_step(self, desire):
        # attach dependant part to request URL (ex. restaurant)
        url = self.common_url + desire + "&key=" + self.API_key
        # go fetch the json object for nearby search
        response = urllib.request.urlopen(url).read()
        # format the json in dict, list, dict, list....
        json_file = simplejson.loads(response)
        # extract the result and place_id of the places near
        for row in json_file["results"]:
            # https://developers.google.com/places/web-service/search#nearby-search-and-text-search-responses
            spaced_name = row["name"]
            name = spaced_name.replace(" ","+")
            self.names.append(name)
            self.place_id[name] = row["place_id"]

    def get_shopping_mall(self):
        # return the option "shopping_mall" to common_step to request nearby "shopping_mall"
        desire = "shopping_mall"
        self.common_step(desire)
        return self.names

    def get_restaurant(self):
        # return the option "restaurant" to common_step to request nearby "restaurant"
        desire = "restaurant"
        self.common_step(desire)
        return self.names

    def get_gas_station(self):
        # return the option "gas_station" to common_step to request nearby "gas_station"
        desire = "gas_station"
        self.common_step(desire)
        return self.names

    def get_hospital(self):
        # return the option "hospital" to common_step to request nearby "hospital"
        desire = "hospital"
        self.common_step(desire)
        return self.names

    def get_parking(self):
        # return the option "parking" to common_step to request nearby "parking"
        desire = "parking"
        self.common_step(desire)
        return self.names

    def get_place_id(self):
        # returns the place_id of the places extracted from the json object
        return self.place_id

    def current_location(self):
        # returns the current location of the user
        return [self.lat, self.lng]
