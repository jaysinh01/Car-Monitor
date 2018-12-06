# $ sudo pip3 install requests
# $ sudo pip3 install arrow
# -*- coding: utf-8 -*-
import requests
import re
import arrow


class weatherInfo:
    '''
    Returns the current weather & local time of a given address
    '''

    def __init__(self, address):
        # address format: city province (optional) country (optional)
        self.address = address.strip()
        # The weather info would be stored in self.message
        self.message = []

    def getLocalTime(self, timeZone):
        # Finds the current time of a given timeZone
        # Gets the current UTC time
        utc = arrow.utcnow()
        # Shifts to the local time
        localTime = utc.to(timeZone).format('YYYY-MM-DD HH:mm:ss')
        return localTime

    def getRawHTML(self, Url):
        # Debug mode
        # Downloads HTML from a given URL & writes the content to RawHTML.txt
        with open('RawHTML.txt', 'w') as rawData:
            # .text method translates the content into a human readable format
            content = requests.get(Url).text
            rawData.write(content)

    def getWeather(self):
        # Searches a city by its name & province & country
        # The URL refers to a specific city in Google Map would be
        # https://www.google.com/maps/place/Edmonton,+AB,+Canada
        googleMapUrl = 'https://www.google.com/maps/place/'
        for i in self.address.split():
            googleMapUrl += (',+' + i)
        # Gets HTML from a given URL
        rawData = requests.get(googleMapUrl)
        # The temperature info in the HTML would be
        # weather/32/sunny.png\",\"Clear\",\"11°C\",\"52°F\",1]\n,null
        rawTempData = re.search(r'weather.+?null', rawData.text).group()
        # tempData = ['Clear', '11°C', '52°F']
        tempData = re.findall(r',\\"(.+?)\\"', rawTempData)
        # The local time info in the HTML would be
        # [[\"America/Edmonton\",[\"MST\",\"Mountain Standard Time\",
        # \"MDT\",\"Mountain Daylight Time\"]\n
        # timeZone = 'America/Edmonton'
        timeZone = re.findall(
            r'\[\[\\"([A-Za-z]+?/[A-Za-z].+?)\\",\[\\"...\\",\\"',
            rawData.text
        )
        # Finds the local time according to its time zone
        tempData.append(self.getLocalTime(timeZone[0]))
        return tempData

    def sendInfo(self):
        # Stores the weather info in self.message
        try:
            self.message.append('Weather in %s:' % self.address)
            tempData = self.getWeather()
            self.message.append('%s, %s, %s' % (
                tempData[0], tempData[1], tempData[2]))
            self.message.append('Local time: %s' % (tempData[3]))
        except AttributeError:
            self.message[0] = (
                "Google Map doesn't have the current weather data..."
                "Failed to access the local weather"
            )
