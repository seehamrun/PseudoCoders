import api
import json
import logging
from google.appengine.api import urlfetch


#inputs placeID and returns JSON with place details
def fetchPlaceDetails(placeID):
    google_url = "https://cors.io/?" + "https://maps.googleapis.com/maps/api/place/details/%s?key=%s&placeid=%s" % ("json", api.googleKey, placeID)
    logging.info(placeID)
    logging.info(google_url)
    urlContent = urlfetch.fetch(google_url).content
    response = json.loads(urlContent)
    return response['result']

#inputs search query and returns any amount of data
def findPlaceRequest(query):
    newQuery = query.replace(" ", "+")
    google_url = "https://cors.io/?" + "https://maps.googleapis.com/maps/api/place/findplacefromtext/%s?input=%s&inputtype=textquery&key=%s&fields=%s" % ("json", newQuery, api.googleKey, getFields())
    urlContent = urlfetch.fetch(google_url).content
    response = json.loads(urlContent)
    logging.info(response)
    response = response['candidates'][0]
    newList = []
    newList.append(response['place_id'])
    newList.append(response['name'])
    newList.append(response['formatted_address'])
    newList.append(response['types'])
    newList.append(response['opening_hours'])
    newList.append(response['price_level'])
    newList.append(response['rating'])
    return newList

#sets the fields returned by helper above, only necessary field is place ID
def getFields():
    output = ""
    output += "name,"
    output += "formatted_address,"
    #output += "geometry,"
    #output += "icon,"
    #output += "id,"
    #output += "name,"
    #output += "permanently_closed,"
    #output += "photos,"
    output += "place_id,"
    #output += "plus_code,"
    #output += "scope,"
    output += "types,"
    output += "opening_hours,"
    output += "price_level,"
    output += "rating,"
    return output[:-1]


#takes latitude/longitude -> can be computed from other Google API
#also inputs a search query
def nearbySearchRequest(location, radius):
    google_url = "https://cors.io/?" + "https://maps.googleapis.com/maps/api/place/nearbysearch/%s?key=%s&location=%s&radius=%s" % ("json", api.googleKey, getLatitudeLongitude(location), radius)
    urlContent = urlfetch.fetch(google_url).content
    response = json.loads(urlContent)
    response = response['results']
    #logging.info(google_url)
    newList = []
    for item in response:
        output = []
        place_id = item['place_id']
        place_details = fetchPlaceDetails(place_id)
        results = place_details
        output.append("PLACE_ID: " + str(place_id))
        if ('name' in results):
            output.append("NAME: " + str(results['name']))
        if ('formatted_address' in results):
            output.append("ADDRESS: " + str(results['formatted_address']))
        if ('types' in results):
            output.append("TYPE: " + str(results['types']))
        if ('opening_hours' in results):
            output.append("HOURS: " + str(results['opening_hours']))
        if ('price_level' in results):
            output.append("PRICE: " + str(results['price_level']))
        if ('rating' in results):
            output.append("RATING: " + str(results['rating']))
        newList.append(output)

    return newList


def nearbySearchRequestFiltered(location, radius, price, type):
    google_url = "https://cors.io/?" + "https://maps.googleapis.com/maps/api/place/nearbysearch/%s?key=%s&location=%s&radius=%s&type=%s&minprice=%s&maxprice=%s" % ("json", api.googleKey, getLatitudeLongitude(location), radius, type, price, price)
    urlContent = urlfetch.fetch(google_url).content
    response = json.loads(urlContent)
    response = response['results']
    #logging.info(google_url)
    newList = []
    for item in response:
        output = []
        place_id = item['place_id']
        place_details = fetchPlaceDetails(place_id)
        results = place_details
        output.append("PLACE_ID: " + str(place_id))
        if ('name' in results):
            output.append("NAME: " + str(results['name']))
        if ('formatted_address' in results):
            output.append("ADDRESS: " + str(results['formatted_address']))
        if ('types' in results):
            output.append("TYPE: " + str(results['types']))
        if ('opening_hours' in results):
            output.append("HOURS: " + str(results['opening_hours']))
        if ('price_level' in results):
            output.append("PRICE: " + str(results['price_level']))
        if ('rating' in results):
            output.append("RATING: " + str(results['rating']))
        newList.append(output)

    return newList



#def getLatitudeLongitude(first_line, city, state):
def getLatitudeLongitude(location):
    newLocation = location.replace(" ", "+")
    #google_url = "https://cors.io/?" + "https://maps.googleapis.com/maps/api/geocode/json?address=%s,%s,%s&key=%s" % (first_line, city, state, api.googleKey)
    google_url = "https://cors.io/?" + "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (newLocation, api.googleKey)
    urlContent = urlfetch.fetch(google_url).content
    #logging.info(urlContent)
    response = json.loads(urlContent)
    #return google_url
    pair = response['results'][0]['geometry']['location']['lat'], response['results'][0]['geometry']['location']['lng']
    return str(pair)[1:-1].replace(" ","")
