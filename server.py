# https://bottlepy.org/docs/dev/
# https://bottlepy.org/docs/dev/tutorial_app.html

# $ sudo pip3 install bottle

# -*- coding: utf-8 -*-
from bottle import route, run, debug, template, request, static_file, error
import weatherScrape
from maps_classes import NearBy
from direction_classes import Directions, check_place

place_id = {}
country = []
city = []


@route('/startMenu')
def callFunction():
    if request.GET.search:
        if request.GET.functions == 'weatherSearch':
            return template('weatherSearch.tpl', result='')
        if request.GET.functions == 'maps':
            return template('maps.tpl')
    return template('startMenu.tpl')


@route('/weatherSearch')
def weatherSearch():
    result = ''
    if request.GET.search:
        location = request.GET.address.strip()
        result = weatherScrape.weatherInfo(location)
    elif request.GET.backToStartMenu:
        return template('startMenu.tpl')
    return template('weatherSearch.tpl', result=result)


@route('/maps')
def maps_page1():
    if request.GET.nearby:
        return template("nearby.tpl")
    if request.GET.find_destination:
        return template("find_destination.tpl")
    elif request.GET.backToStartMenu:
        return template('startMenu.tpl')
    return template('maps.tpl')


@route('/nearby')
def nearby():
    global class_initialize
    class_initialize = NearBy()
    global place_id
    global results
    if request.GET.restuarant:
        results = class_initialize.get_restaurant()
        place_id = class_initialize.get_place_id()
        return template("nearby_result.tpl", result=results)
    if request.GET.shopping_mall:
        results = class_initialize.get_shopping_mall()
        place_id = class_initialize.get_place_id()
        return template("nearby_result.tpl", result=results)
    if request.GET.gas_station:
        results = class_initialize.get_gas_station()
        place_id = class_initialize.get_place_id()
        return template("nearby_result.tpl", result=results)
    if request.GET.hospital:
        results = class_initialize.get_hospital()
        place_id = class_initialize.get_place_id()
        return template("nearby_result.tpl", result=results)
    if request.GET.parking:
        results = class_initialize.get_parking()
        place_id = class_initialize.get_place_id()
        return template("nearby_result.tpl", result=results)
    elif request.GET.backToStartMenu:
        return template('startMenu.tpl')
    return template("nearby.tpl")


@route('/nearby/results')
def near_result():
    global place_id
    for place in place_id.keys():
        global instruction
        # make the value the same
        if request.GET.place == place:
            direction = Directions(place_id[place])
            json_file = direction.json_object()
            instruction = direction.get_directions(json_file)
            return template("directions.tpl", intructions=instruction)
        elif request.GET.backToStartMenu:
            return template('startMenu.tpl')
    return template("nearby_result.tpl", result=results)


@route('/directions')
def directions_nearby():
    if request.GET.backToStartmenu:
        return template("startMenu.tpl")
    elif request.GET.back:
        return template("nearby_result.tpl")
    return template("directions.tpl", instructions=instruction)


@route('/find_destination')
def find_destination():
    if request.GET.enter_destination:
        return template("country.tpl")
    if request.GET.back:
        return template("maps.tpl")
    # implement the other feature here
    return template("find_destination.tpl")


@route('/find_destination/country')
def country():
    global country
    if request.GET.enter:
        country = request.GET.country.strip()
        return template("city.tpl")
    # back options left
    return template("country.tpl")


@route('/find_destination/country/city/')
def city():
    global city
    if request.GET.enter:
        city = request.GET.city.strip()
        return template("enter_address.tpl")
    # back fetures
    return template("city.tpl")


@route("/find_destination/country/city/address")
def street_adresss():
    global address
    global suggested_address
    if request.GET.enter:
        address = request.GET.address
        # make an error statement for country
        suggested_address = check_place(country[0], city[0], address)
        return template("validate_place", address=suggested_address)
    return template("enter_address.tpl")


@route("/find_destination/country/city/address/validate_address")
def validation():
    if request.GET.select:

        return template("country.tpl")
    if request.GET.back:
        return template("enter_address.tpl")
    elif request.GET.backToStartMenu:
        return template('startMenu.tpl')
    return template("validate_place.tpl", address=suggested_address)


@route('/find_destination/destination/country')
def country():
    global country
    if request.GET.enter:
        country = request.GET.country.strip()
        return template("city.tpl")
    if request.GET.back:
        return template("validate_place.tpl", address=suggested_address)
    elif request.GET.backToStartMenu:
        return template('startMenu.tpl')
    return template("country.tpl")


@route('/find_destination/destination/country/city/')
def city():
    global city
    if request.GET.enter:
        city = request.GET.city.strip()
        return template("enter_address.tpl")
    # back fetures
    return template("city.tpl")


@route("/find_destination/destination/country/city/address")
def street_address():
    global address
    global destination_suggested_address
    if request.GET.enter:
        address = request.GET.address
        # make an error statement for country
        destination_suggested_address = check_place(country[0], city[0], address)
        return template("validate_place", address=destination_suggested_address)
    return template("enter_address.tpl")


@route("/find_destination/destination/country/city/address/validate_address")
def validation():
    if request.GET.select:
        global step_by_step
        directions_from_class = Directions(destination_suggested_address, suggested_address)
        json_object = directions_from_class.json_object()
        step_by_step = directions_from_class.get_directions(json_object)
        return template("directions.tpl",instructions=step_by_step)
    return template("validate_place.tpl", address=destination_suggested_address)


@route("/directions")
def directions():
    if request.GET.back:
        return template("validate_place.tpl", address=destination_suggested_address)
    elif request.GET.backToStartMenu:
        return template('startMenu.tpl')
    return template("directions.tpl", instructions=step_by_step)

# Debug mode
debug(True)

run(port=8080, reloader=True)
