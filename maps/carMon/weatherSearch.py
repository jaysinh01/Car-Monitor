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
        self.address = address.strip()
        self.message = []

    def getLocalTime(self, timeZone):
        # Gets the current UTC time
        utc = arrow.utcnow()
        # Shifts to the local time
        localTime = utc.to(timeZone).format('YYYY-MM-DD HH:mm:ss')
        return localTime

    def getRawHTML(self, Url):
        # Debug mode
        # Downloads HTML from a given URL and writes the content to RawHTML.txt
        with open('RawHTML.txt', 'w') as rawData:
            # .text method translates the content into a human readable format
            content = requests.get(Url).text
            rawData.write(content)

    def getWeather(self):
        # Searches a city by its name & province & country
        # https://www.google.com/maps/place/Edmonton,+AB,+Canada
        googleMapUrl = 'https://www.google.com/maps/place/'
        for i in self.address.split():
            googleMapUrl += (',+' + i)
        rawData = requests.get(googleMapUrl)
        # Debug mode
        # self.getRawHTML(googleMapUrl)
        # Temperature in
        # weather/32/sunny.png\",\"Clear\",\"11°C\",\"52°F\",1]\n,null
        # tempData = ['Clear', '11°C', '52°F']
        rawTempData = re.search(r'weather.+?null', rawData.text).group()
        tempData = re.findall(r',\\"(.+?)\\"', rawTempData)
        # Local time in
        # [[\"America/Edmonton\",[\"MST\",\"Mountain Standard Time\",
        # \"MDT\",\"Mountain Daylight Time\"]\n
        # timeZone = 'America/Edmonton'
        timeZone = re.findall(
            r'\[\[\\"([A-Za-z]+?/[A-Za-z].+?)\\",\[\\"...\\",\\"',
            rawData.text
        )
        tempData.append(self.getLocalTime(timeZone[0]))
        return tempData

    def sendInfo(self):
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
