# https://bottlepy.org/docs/dev/
# https://bottlepy.org/docs/dev/tutorial_app.html

# $ sudo pip3 install bottle

# -*- coding: utf-8 -*-
from bottle import route, run, debug, template, request, static_file, error
from maps_classes import NearBy
from direction_classes import Directions, check_place

place_id = {}
instruction = {}

@route('/startMenu')
def callFunction():
    if request.GET.search:
        if request.GET.functions == 'maps':
            return template('maps.tpl', suggestedAddress = "")
    return template('startMenu.tpl')


@route('/maps')
def guide():
    global place_id
    global results
    class_initialize = NearBy()
    suggested_address = ''
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
            return template("nearbyResults.tpl", result = results)
    if request.GET.findDestination:
        address = request.GET.address.strip()
        city = request.GET.city.strip()
        country = request.GET.country.strip()
        # make an error statement for country
        suggested_address = check_place(country, city, address)
    if request.GET.goBySuggestions:
        directions_from_class = Directions(suggested_address)
        json_object = directions_from_class.json_object()
        step_by_step = directions_from_class.get_directions(json_object)
        return template("directions.tpl", instructions = step_by_step)
    if request.GET.backToStartMenu:
        return template('startMenu.tpl')
    return template('maps.tpl', suggestedAddress = suggested_address)


@route('/nearbyResults')
def nearbyResults():
    global place_id
    global instruction
    if request.GET.direction:
        placeName = request.GET.place
        print(place_id[placeName])
        direction = Directions(place_id[placeName])
        json_file = direction.json_object()
        instruction = direction.get_directions(json_file)
        return template("directions.tpl", instructions = instruction["directions"])
    if request.GET.backToPrev:
        return template('maps.tpl')
    if request.GET.backToStartMenu:
        return template('startMenu.tpl')
    return template("nearbyResults.tpl", result = results)


@route('/directions')
def directions():
    global instruction
    if request.GET.backToPrev:
        return template("nearbyResults.tpl")
    if request.GET.backToStartmenu:
        return template("startMenu.tpl")
    return template("directions.tpl", instructions = instruction["directions"])


# Debug mode
debug(True)

run(port=8080, reloader=True)
