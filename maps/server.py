# https://bottlepy.org/docs/dev/
# https://bottlepy.org/docs/dev/tutorial_app.html

# $ sudo pip3 install bottle

# -*- coding: utf-8 -*-
from bottle import route, run, debug, template, request, static_file, error
from maps_classes import NearBy
from direction_classes import Directions, check_place

place_id = {}
instruction = {}
results = []
address_id = 0

@route('/startMenu')
def callFunction():
    if request.GET.search:
        if request.GET.functions == 'maps':
            return template('maps.tpl', suggestedAddress = '')
    return template('startMenu.tpl')


@route('/maps')
def guide():
    global place_id
    global results
    global instruction
    class_initialize = NearBy()
    suggested_address = ''
    global address_id
    if request.GET.searchNearby:
        if request.GET.nearby == 'Restuarant':
            results = class_initialize.get_restaurant()
            place_id = class_initialize.get_place_id()
            return template("nearbyResults.tpl", result = results)
        elif request.GET.nearby == 'ShoppingMalls':
            results = class_initialize.get_shopping_mall()
            place_id = class_initialize.get_place_id()
            return template("nearbyResults.tpl", result = results)
        elif request.GET.nearby == 'GasStations':
            results = class_initialize.get_gas_station()
            place_id = class_initialize.get_place_id()
            return template("nearbyResults.tpl", result = results)
        elif request.GET.nearby == 'Hospital':
            results = class_initialize.get_hospital()
            place_id = class_initialize.get_place_id()
            return template("nearbyResults.tpl", result = results)
        elif request.GET.nearby == 'ParkingSpots':
            results = class_initialize.get_parking()
            place_id = class_initialize.get_place_id()
            if results is None:
                results = "The address is not valid"
            return template("nearbyResults.tpl", result = results)
    if request.GET.findDestination:
        address = request.GET.address.strip()
        address = address.replace(" ","+")
        print(address)
        city = request.GET.city.strip()
        country = request.GET.country.strip()
        # make an error statement for country
        suggested_address, address_id = check_place(country, city, address)
        if suggested_address is None:
          suggested_address = "The address is invalid"
    if request.GET.goBySuggestion:
        directions_from_class = Directions(str(address_id))
        json_object = directions_from_class.json_object()
        instruction = directions_from_class.get_directions(json_object)
        return template("directions.tpl", instructions = instruction)
    if request.GET.backToStartMenu:
        return template('startMenu.tpl')
    return template('maps.tpl', suggestedAddress = suggested_address)


@route('/nearbyResults')
def nearbyResults():
    global place_id
    global instruction
    if request.GET.direction:
        placeName = request.GET.place.strip()
        direction = Directions(place_id[placeName])
        json_file = direction.json_object()
        instruction = direction.get_directions(json_file)
        return template("directions.tpl", instructions = instruction)
    if request.GET.backToPrev:
        return template('maps.tpl', suggestedAddress = '')
    if request.GET.backToStartMenu:
        return template('startMenu.tpl')
    return template("nearbyResults.tpl", result = results)


@route('/directions')
def directions():
    global instruction
    if request.GET.backToPrev:
        return template("nearbyResults.tpl", result = results)
    if request.GET.backToStartMenu:
        return template("startMenu.tpl")
    return template("directions.tpl", instructions = instruction)


# Debug mode
debug(True)

run(port=8080, reloader=True)
