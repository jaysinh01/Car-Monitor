
def the_url(elements_dictionary):
    url = "https://maps.googleapis.com/maps/api/directions/json?"
    for x, y in elements_dictionary.items():
        url = url + x + '=' + y
        url += "&"
    url = url[:-1]
    print(url)


def main():
    '''' THis function will generate tokens needed to to generate a request url'''
# all the requests will be stored in here
    url_dictionary = {}
# Asking for the option
    choice = (input("would you prefer Bus or Car? "))
    print("Excellent")
    print("please enter your address\nEg: 1109 59a street SouthWest T6X0T2 Edmonton AB")
    origin_string = input(" ")
    # Replacing and editing input to use it effortlessly for URL requests.
    origin = origin_string.replace(" ","+")
    url_dictionary["origin"] = origin
    destination_string = input("Please enter your destination. Ensure format is similar to the example shown above: ")
    destination = destination_string.replace(" ","+")
    url_dictionary["destination"] = destination
    url_dictionary["mode"] = choice
    the_url(url_dictionary)


if __name__ == '__main__':

    main()
