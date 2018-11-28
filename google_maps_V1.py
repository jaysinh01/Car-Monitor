import urllib.request
import json
import simplejson
import re


'''This version will dump all the features in to one file. Later, it will be organized and optimized'''


def the_url(elements_dictionary):
    url = "https://maps.googleapis.com/maps/api/directions/json?"
    for category, user_input in elements_dictionary.items():
        url = url + category + '=' + user_input
        url += "&"
    API_key = 'AIzaSyCT4l0QIAEcuZbM9M2ZnciH7Cq8M3jQ_nw'
    url += "key=" + API_key
    # print(url)
    response = urllib.request.urlopen(url).read()
    json_object = simplejson.loads(response)
    # response = requests.get(url).json()
    with open(elements_dictionary["origin"] + elements_dictionary["destination"] + ".json", "w") as result:
            simplejson.dump(json_object, result)
    with open("history.txt", "a+") as history:
            history.write(elements_dictionary["origin"] + "\n")
            history.write(elements_dictionary["destination"] + "\n")
    return json_object


def main():
    """ THis function will generate tokens needed to to generate a request url """
# all the requests will be stored in here
    url_dictionary = {}
# Asking for the option
    choice = (input("would you prefer Bus or Car? "))
    print("Excellent")
    print("please enter your address\nEx: 1109 59a street SouthWest T6X0T2 Edmonton AB")
    origin_string = input(" ")
    # Replacing and editing input to use it effortlessly for URL requests.
    origin = origin_string.replace(" ","+")
    url_dictionary["origin"] = origin.lower()
    destination_string = input("Please enter your destination. Ensure format is similar to the example shown above:\n")
    destination = destination_string.replace(" ","+")
    url_dictionary["destination"] = destination.lower()
    url_dictionary["mode"] = choice.lower()
    try:
      with open(url_dictionary["origin"] + url_dictionary["destination"] + ".json") as pervious_search:
        json_string = json.loads(pervious_search)
        reading_from_json(json_string)
    except:
      try:
        result_dict = the_url(url_dictionary)
        with open(url_dictionary["origin"] + url_dictionary["destination"] + ".json", "w") as new_file:
          reading_from_json(result_dict)

      except:
        print("Please check the address again")


def reading_from_json(json_file):
    ''' this function will read desired information from JSON file '''

    total_time = 0
    total_distance = 0
    for row in json_file["routes"][0]["legs"][0]["steps"]:
        direction = row['html_instructions']
        distance = row['distance']['text']
        duration = row['duration']['text']
        total_time += duration
        total_distance += distance
        html_tags = re.findall('<[^<]+?>', direction)
        for remove in html_tags:
            direction = direction.replace(remove, "")
        print(direction + " in " + distance + " in about " + duration)
    print("The total distance is " + total_distance)
    print("The total duration is " + total_time)


if __name__ == '__main__':
  main()

