# $ sudo pip3 install bottle
# server.py creates local web pages by implementing python library bottle
# The idea of the script is using HTML as the front backed up by python
# Every @route('/') is corresponding to a URL
# e.g. @route('/startMenu') <=> http://localhost:8080/startMenu
# The function under the route would be called automatically
# when the user visits that URL, and the template for that web page
# would be returned
# More info:
# https://bottlepy.org/docs/dev/
# https://bottlepy.org/docs/dev/tutorial_app.html
# -*- coding: utf-8 -*-
from bottle import route, run, debug, template, request, static_file, error
from weatherSearch import weatherInfo
from musicPlayer import musicLib
from maps_classes import NearBy
from direction_classes import Directions, check_place

# Global values results & place_id & instructions
# would be passed/accessed between different website route
results = []
place_id = {}
instructions = {}


@route('/startMenu')
def callFunction():
    # startMenu page
    # Initializes the playlist
    songLib = musicLib()
    songLib.creatPlaylist()
    # If 'search' button is clicked
    if request.GET.search:
        # If 'musicPlayer' button is chosen
        if request.GET.functions == 'musicPlayer':
            # Goto @route('/musicPlayer')
            return template(
                'musicPlayer.tpl',
                autoPlay='',
                playlist=songLib.playlist
            )
        # If 'weatherSearch' button is chosen
        elif request.GET.functions == 'weatherSearch':
            # Goto @route('/weatherSearch')
            return template('weatherSearch.tpl', result='')
        # If 'maps' button is chosen
        elif request.GET.functions == 'maps':
            # Goto @route('/maps')
            return template('maps.tpl', suggestedAddress='')
    return template('startMenu.tpl')


@route('/weatherSearch')
def weatherSearch():
    result = ''
    # If 'search' button is clicked
    if request.GET.search:
        # Gets the address that the user typed
        location = request.GET.address.strip()
        # Gets the corresponding info
        localWeather = weatherInfo(location)
        localWeather.sendInfo()
        result = localWeather.message
    # Back to @route('/startMenu')
    elif request.GET.backToStartMenu:
        return template('startMenu.tpl')
    return template('weatherSearch.tpl', result=result)


@route('/static/<filename:re:.*>')
def staticServer(filename):
    # Code varied from:
    # https://stackoverflow.com/questions/10486224/bottle-static-files
    # Serves the files in directory './static' to an URL
    # which could be accessed by other web pages
    # e.g. file 'whatever.mp3' could be accessed from URL
    # http://localhost:8080/static/whatever.mp3
    # Note: file name could not contain blank space
    return static_file(filename, root='./static')


@route('/musicPlayer')
def musicPlayer():
    # If autoPlay == 'autoPlay'
    # songs in @route('/musicPlayer') would be auto played
    autoPlay = ''
    # Gets the playlist
    songLib = musicLib()
    songLib.playlist = songLib.getInfo('playlistStream')
    # The 'refresh' button would be clicked automatically
    # after a song has finished playing
    if request.GET.refresh:
        # .writeFreqDict()
        # records the number of times a song has been played
        songLib.writeFreqDict(songLib.playlist[0])
        # Plays next song
        songLib.shiftList(1)
    # If 'next' button is clicked
    if request.GET.next:
        # Plays next song
        songLib.shiftList(1)
    # If 'prevSong' button is clicked
    if request.GET.prevSong:
        # Plays previous song
        songLib.shiftList(len(songLib.playlist) - 1)
    # If 'preference' button is clicked
    if request.GET.preference:
        # The playlist would be sorted by
        # the # of times each song is played
        songLib.freqList()
    # If 'goTo' button is clicked
    if request.GET.goTo:
        # Plays the selected song immediately
        songIndex = int(request.GET.song.strip())
        songLib.shiftList(songIndex)
    # Determines whether the user chooses 'autoPlay' mode
    autoPlay = request.GET.autoPlaySelect.strip()
    # Back to @route('/startMenu')
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
    # If 'searchNearby' button is clicked
    if request.GET.searchNearby:
        # If 'Restaurant' button is chosen
        if request.GET.nearby.strip() == 'Restaurant':
            # Gets nearby restaurants' info (name & ID)
            results = nearbyClass.get_restaurant()
            place_id = nearbyClass.get_place_id()
            # Goto @route('/nearbyResults')
            return template('nearbyResults.tpl', results=results)
        # If 'ShoppingMalls' button is chosen
        elif request.GET.nearby.strip() == 'ShoppingMalls':
            results = nearbyClass.get_shopping_mall()
            place_id = nearbyClass.get_place_id()
            return template('nearbyResults.tpl', results=results)
        # If 'GasStations' button is chosen
        elif request.GET.nearby.strip() == 'GasStations':
            results = nearbyClass.get_gas_station()
            place_id = nearbyClass.get_place_id()
            return template('nearbyResults.tpl', results=results)
        # If 'Hospital' button is chosen
        elif request.GET.nearby.strip() == 'Hospital':
            results = nearbyClass.get_hospital()
            place_id = nearbyClass.get_place_id()
            return template('nearbyResults.tpl', results=results)
        # If 'ParkingSpots' button is chosen
        elif request.GET.nearby.strip() == 'ParkingSpots':
            results = nearbyClass.get_parking()
            place_id = nearbyClass.get_place_id()
            return template('nearbyResults.tpl', results=results)
    # If 'findDestination' button is clicked
    if request.GET.findDestination:
        # Gets the address that the user typed
        address = request.GET.address.strip().replace(' ', '+')
        city = request.GET.city.strip().replace(' ', '+')
        country = request.GET.country.strip().replace(' ', '+')
        # Gets the suggested address which is accessible using Google MAP
        # according to the typed address
        suggested_address, address_id = check_place(country, city, address)
        # If the typed address is invalid
        if suggested_address is None:
            suggested_address = 'The address is invalid'
        else:
            # Finds the corresponding address ID
            directions_from_class = Directions(str(address_id))
            json_object = directions_from_class.json_object()
            # From Google API gets the navigations (instructions)
            # by providing the current location's IP & destination's ID
            instructions = directions_from_class.get_directions(json_object)
    # Goto @route('/directions')
    if request.GET.goBySuggestion:
        return template('directions.tpl', instructions=instructions)
    # Goto @route('/startMenu')
    if request.GET.backToStartMenu:
        return template('startMenu.tpl')
    return template('maps.tpl', suggestedAddress=suggested_address)


@route('/nearbyResults')
def nearbyresults():
    # The nearby results would be showed
    # as a list which the user could select
    # one of the destinations
    global results
    global place_id
    global instructions
    # If 'direction' button is clicked
    if request.GET.direction:
        # Gets the selected place's name
        placeName = request.GET.place.strip()
        # It's corresponding ID is in the dictionary 'place_id'
        # place_id[placeName] == correspondingID
        # From Google API gets the navigations (instructions)
        # by providing the current location's IP & destination's ID
        direction = Directions(place_id[placeName])
        json_file = direction.json_object()
        instructions = direction.get_directions(json_file)
        # Goto @route('/directions')
        return template('directions.tpl', instructions=instructions)
    # Goto @route('/maps')
    if request.GET.backToPrev:
        return template('maps.tpl', suggestedAddress='')
    # Goto @route('/startMenu')
    if request.GET.backToStartMenu:
        return template('startMenu.tpl')
    return template('nearbyResults.tpl', results=results)


@route('/directions')
def directions():
    # Shows the navigations (instructions)
    global instructions
    # Goto @route('/maps')
    if request.GET.backToPrev:
        return template('maps.tpl', suggestedAddress='')
    # Goto @route('/startMenu')
    if request.GET.backToStartMenu:
        return template('startMenu.tpl')
    return template('directions.tpl', instructions=instructions)


# Debug mode
debug(True)

run(port=8080, reloader=True)
