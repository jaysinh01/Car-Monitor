# $ pip install requests
# $ sudo pip3 install arrow

# -*- coding: utf-8 -*-
import requests
import re
import arrow

# http://zetcode.com/python/arrow/
def getLocalTime (timeZone):
    utc = arrow.utcnow()
    localTime = utc.to(timeZone).format('YYYY-MM-DD HH:mm:ss')
    return localTime

# Debug mode
def getRawHTML (Url):
    with open('RawHTML.txt', 'w') as rawData:
        content = requests.get(Url).text
        rawData.write(content)

def getWeather (address):
    headers = {'user-agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36')}
    # Searches a city by its name & province & country
    # https://www.google.com/maps/place/Edmonton,+AB,+Canada
    googleMapUrl = "https://www.google.com/maps/place/"
    for i in address:
        googleMapUrl += (',+' + i)
    rawData = requests.get(googleMapUrl, headers = headers)
    # Debug mode
    # getRawHTML(googleMapUrl)
    # Temperature in
    # weather/32/sunny.png\",\"Clear\",\"11°C\",\"52°F\",1]\n,null
    # weather/32/partly_cloudy.png\",\"Partly Cloudy\",\"17°C\",\"62°F\",1]\n,null
    # tempData = ['Clear', '11°C', '52°F']
    rawTempData = re.search(r'weather.+?null', rawData.text).group()
    tempData = re.findall(r',\\"(.+?)\\"', rawTempData)
    # Local time in
    # [[\"America/Edmonton\",[\"MST\",\"Mountain Standard Time\",\"MDT\",\"Mountain Daylight Time\"]\n
    # [[\"America/Los_Angeles\",[\"PST\",\"Pacific Standard Time\",\"PDT\",\"Pacific Daylight Time\"]\n
    # timeZone = 'America/Edmonton'
    timeZone = re.findall(r'\[\[\\"([A-Za-z]+?/[A-Za-z].+?)\\",\[\\"...\\",\\"', rawData.text)
    tempData.append(getLocalTime(timeZone[0]))
    return tempData

def weatherInfo (address):
    message = []
    try:
        message.append("Weather in %s:" % address)
        address = address.split()
        tempData = getWeather(address)
        message.append("%s, %s, %s" % (tempData[0], tempData[1], tempData[2]))
        message.append("Local time: %s" % (tempData[3]))
    except AttributeError:
        message[0] = ("Failed to access the local weather...Try another city")
    return message
