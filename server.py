# https://bottlepy.org/docs/dev/
# https://bottlepy.org/docs/dev/tutorial_app.html
# $ sudo pip3 install bottle
# -*- coding: utf-8 -*-
from bottle import route, run, debug, template, request, static_file, error
from weatherSearch import weatherInfo
from musicPlayer import musicLib
from maps_classes import NearBy
from direction_classes import Directions, check_place

results = []
place_id = {}
instructions = {}


@route('/startMenu')
def callFunction():
    songLib = musicLib()
    songLib.creatPlaylist()
    if request.GET.search:
        if request.GET.functions == 'musicPlayer':
            return template(
                'musicPlayer.tpl',
                autoPlay='',
                playlist=songLib.playlist
            )
        elif request.GET.functions == 'weatherSearch':
            return template('weatherSearch.tpl', result='')
        elif request.GET.functions == 'maps':
            return template('maps.tpl', suggestedAddress='')
    return template('startMenu.tpl')


@route('/weatherSearch')
def weatherSearch():
    result = ''
    if request.GET.search:
        location = request.GET.address.strip()
        localWeather = weatherInfo(location)
        localWeather.sendInfo()
        result = localWeather.message
    elif request.GET.backToStartMenu:
        return template('startMenu.tpl')
    return template('weatherSearch.tpl', result=result)


# https://stackoverflow.com/questions/10486224/bottle-static-files
@route('/static/<filename:re:.*>')
def staticServer(filename):
    return static_file(filename, root='./static')


@route('/musicPlayer')
def musicPlayer():
    autoPlay = ''
    songLib = musicLib()
    songLib.playlist = songLib.getInfo('playlistStream')
    if request.GET.refresh:
        songLib.writeFreqDict(songLib.playlist[0])
        songLib.shiftList(1)
    if request.GET.next:
        songLib.shiftList(1)
    if request.GET.prevSong:
        songLib.shiftList(len(songLib.playlist) - 1)
    if request.GET.preference:
        songLib.freqList()
    if request.GET.goTo:
        songIndex = int(request.GET.song.strip())
        songLib.shiftList(songIndex)
    autoPlay = request.GET.autoPlaySelect.strip()
    if request.GET.backToStartMenu:
        return template('startMenu.tpl')
    return template(
        'musicPlayer.tpl',
        autoPlay=autoPlay,
        playlist=songLib.playlist
    )


@route('/maps')
def guide():
    global results
    global place_id
    global instructions
    suggested_address = ''
    nearbyClass = NearBy()
    if request.GET.searchNearby:
        if request.GET.nearby.strip() == 'Restuarant':
            results = nearbyClass.get_restaurant()
            place_id = nearbyClass.get_place_id()
            return template('nearbyResults.tpl', results=results)
        elif request.GET.nearby.strip() == 'ShoppingMalls':
            results = nearbyClass.get_shopping_mall()
            place_id = nearbyClass.get_place_id()
            return template('nearbyResults.tpl', results=results)
        elif request.GET.nearby.strip() == 'GasStations':
            results = nearbyClass.get_gas_station()
            place_id = nearbyClass.get_place_id()
            return template('nearbyResults.tpl', results=results)
        elif request.GET.nearby.strip() == 'Hospital':
            results = nearbyClass.get_hospital()
            place_id = nearbyClass.get_place_id()
            return template('nearbyResults.tpl', results=results)
        elif request.GET.nearby.strip() == 'ParkingSpots':
            results = nearbyClass.get_parking()
            place_id = nearbyClass.get_place_id()
            return template('nearbyResults.tpl', results=results)
    if request.GET.findDestination:
        address = request.GET.address.strip().replace(' ', '+')
        city = request.GET.city.strip().replace(' ', '+')
        country = request.GET.country.strip().replace(' ', '+')
        suggested_address, address_id = check_place(country, city, address)
        if suggested_address is None:
            suggested_address = 'The address is invalid'
        else:
            directions_from_class = Directions(str(address_id))
            json_object = directions_from_class.json_object()
            instructions = directions_from_class.get_directions(json_object)
    if request.GET.goBySuggestion:
        return template('directions.tpl', instructions=instructions)
    if request.GET.backToStartMenu:
        return template('startMenu.tpl')
    return template('maps.tpl', suggestedAddress=suggested_address)


@route('/nearbyResults')
def nearbyresults():
    global results
    global place_id
    global instructions
    if request.GET.direction:
        placeName = request.GET.place.strip()
        direction = Directions(place_id[placeName])
        json_file = direction.json_object()
        instructions = direction.get_directions(json_file)
        return template('directions.tpl', instructions=instructions)
    if request.GET.backToPrev:
        return template('maps.tpl', suggestedAddress='')
    if request.GET.backToStartMenu:
        return template('startMenu.tpl')
    return template('nearbyResults.tpl', results=results)


@route('/directions')
def directions():
    global instructions
    if request.GET.backToPrev:
        return template('maps.tpl', suggestedAddress='')
    if request.GET.backToStartMenu:
        return template('startMenu.tpl')
    return template('directions.tpl', instructions=instructions)


# Debug mode
debug(True)

run(port=8080, reloader=True)
