import google_maps_V1


from bottle import route, run, debug, template, request, static_file, error
import weatherScrape

@route('/weatherSearch', method='GET')
def weatherSearch():
    result = ''
    if request.GET.search:
        address = request.GET.address.strip().split()
        address += ['' for i in range(3 - len(address))]
        result = weatherScrape.server(address[0], address[1], address[2])
    return template('weatherSearch.tpl', result = result)

@route('/maps', method='GET')
def first_page():


# Debug mode
debug(True)
run(port=8080, reloader=True)
