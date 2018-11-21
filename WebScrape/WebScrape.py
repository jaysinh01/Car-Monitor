# Setup procedure:
#   Install selenium:
#       $ sudo apt-get install python3-pip
#       $ sudo pip3 install selenium
#
#   Download geckodriver form:
#       https://github.com/mozilla/geckodriver/releases
#
#   Extract:
#       $ tar -xvzf geckodriver*
#
#   Make it executable:
#       $ chmod +x geckodriver
#
#   Add the driver to your path so other tools can find it:
#       FirefoxPath = "path-to-extracted-file"
#
#   Find the Path:
#       $ find / -xdev -name geckodriver

from selenium import webdriver
FirefoxPath = "/home/cmput274/WebScrape/geckodriver"
browser = webdriver.Firefox(executable_path = FirefoxPath)
with open('weather.txt', 'w') as rawData:
    browser.get("https://www.theweathernetwork.com/ca/weather/alberta/edmonton?wx_auto_reload=")
    rawData.write(browser.page_source)
# weather = '<span class="temp">(.*?)</span>'
# output = re.compile(weather, re.S).findall(line)
# print(output)