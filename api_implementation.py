import api
import json
import logging
import ast
import random
import yaml
import re
import time
from google.appengine.api import urlfetch


#inputs placeID and returns JSON with place details
def fetchPlaceDetails(placeID):
    #google_url = "https://cors.io/?" + "https://maps.googleapis.com/maps/api/place/details/%s?key=%s&placeid=%s" % ("json", api.googleKey, placeID)
    google_url = "https://maps.googleapis.com/maps/api/place/details/%s?key=%s&placeid=%s" % ("json", api.googleKey, placeID)
    # logging.info(placeID)
    # logging.info(google_url)
    urlContent = urlfetch.fetch(google_url).content
    response = json.loads(urlContent)
    return response['result']

#inputs search query and returns any amount of data
def findPlaceRequest(query):
    newQuery = query.replace(" ", "+")
    #google_url = "https://cors.io/?" + "https://maps.googleapis.com/maps/api/place/findplacefromtext/%s?input=%s&inputtype=textquery&key=%s&fields=%s" % ("json", newQuery, api.googleKey, getFields())
    google_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/%s?input=%s&inputtype=textquery&key=%s&fields=%s" % ("json", newQuery, api.googleKey, getFields())
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
    #google_url = "https://cors.io/?" + "https://maps.googleapis.com/maps/api/place/nearbysearch/%s?key=%s&location=%s&radius=%s" % ("json", api.googleKey, getLatitudeLongitude(location), radius)
    google_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/%s?key=%s&location=%s&radius=%s" % ("json", api.googleKey, getLatitudeLongitude(location), radius)
    urlContent = urlfetch.fetch(google_url).content
    response = json.loads(urlContent)
    response = response['results']
    logging.info(google_url)
    newList = []
    for item in response:
        dictionary = {}
        place_id = item['place_id']
        place_details = fetchPlaceDetails(place_id)
        results = place_details
        dictionary["PLACEID"] = place_id
        if ('name' in results):
            dictionary["NAME"] = results['name']
        if ('formatted_address' in results):
            dictionary["ADDRESS"] = results['formatted_address']
        if ('types' in results):
            dictionary["TYPE"] = results['types']
        if ('opening_hours' in results):
            dictionary["HOURS"] = results['opening_hours']
        if ('price_level' in results):
            dictionary["PRICE"] = results['price_level']
        if ('rating' in results):
            dictionary["RATING"] = results['rating']
        newList.append(dictionary)
    return newList

# def get_type(input_data):
#     try:
#         return type(literal_eval(input_data))
#     except (ValueError, SyntaxError):
#         # A string, so return str
#         return str
#
# def fix(input):
#     if not get_type(input) == "<class 'str'>":
#         return input
#     printable = string.printable
#     newString = ""
#     for c in input:
#         if c in printable:
#             newString += c

def nearbySearchRequestFiltered(location, radius, maxprice, type):
    markerA = time.time()

    #google_url = "https://cors.io/?" + "https://maps.googleapis.com/maps/api/place/nearbysearch/%s?key=%s&location=%s&radius=%s&type=%s&minprice=%s&maxprice=%s" % ("json", api.googleKey, getLatitudeLongitude(location), radius, type, 0, maxprice)

    google_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/%s?key=%s&location=%s&radius=%s&type=%s&minprice=%s&maxprice=%s" % ("json", api.googleKey, getLatitudeLongitude(location), radius, type, 0, maxprice)


    urlContent = urlfetch.fetch(google_url).content
    response = json.loads(urlContent)
    response = response['results']
    logging.info(google_url)
    newList = []

    markerB = time.time()
    logging.info("markerB just took " +str(markerB-markerA) + " seconds to run!")

    for index in range(len(response)):
    #for item in response:
        if index > 4:
            break
        item = response[index]
        dictionary = {}
        place_id = item['place_id']
        place_details = fetchPlaceDetails(place_id)
        results = place_details
        dictionary["PLACEID"] = place_id
        if ('name' in results):
            dictionary["NAME"] = fixFormat(results['name'])
        if ('formatted_address' in results):
            dictionary["ADDRESS"] = fixFormat(results['formatted_address'])
        # if ('types' in results):
        #     dictionary["TYPE"] = results['types']
        dictionary["TYPE"] = type.replace("_", " ").title()
        # if ('opening_hours' in results):
        #     dictionary["HOURS"] = results['opening_hours']
        if ('price_level' in results):
            dictionary["PRICE"] = results['price_level']
        if ('rating' in results):
            dictionary["RATING"] = results['rating']

        if not len(dictionary["NAME"]) == 0:
            newList.append(dictionary)
    #time2 = time.clock()
    #logging.info("The runtime of nearbySearchRequestFiltered is " + str(time2-time1))

    markerC = time.time()
    logging.info("markerC just took " +str(markerC-markerB) + " seconds to run!")

    return newList

def fixFormat(stringText):
    # stringText = str(stringText).replace("\u"," ")
    # stringText = str(stringText).replace("u"," ")
    stringText = stringText.encode("utf-8").decode('utf-8').encode('ascii', errors='ignore')
    stringText = re.sub(r'[^\x00-\x7f]',r'', stringText)
    stringText = stringText.replace("\xe2\x80\x99","'")
    stringText = stringText.encode('ascii',errors='ignore')
    return stringText

#def getLatitudeLongitude(first_line, city, state):
def getLatitudeLongitude(location):
    newLocation = location.replace(" ", "+")
    #google_url = "https://cors.io/?" + "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (newLocation, api.googleKey)
    google_url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (newLocation, api.googleKey)
    urlContent = urlfetch.fetch(google_url).content
    #logging.info(urlContent)
    response = json.loads(urlContent)
    #return google_url
    pair = response['results'][0]['geometry']['location']['lat'], response['results'][0]['geometry']['location']['lng']
    return str(pair)[1:-1].replace(" ","")

#types = ['amusement_park', 'aquarium', 'art_gallery', 'bakery', 'bar', 'beauty_salon', 'bowling_alley', 'cafe', 'casino', 'gym', 'library', 'movie_theater', 'museum', 'night_club', 'park', 'restaurant', 'shopping_mall', 'stadium', 'store', 'zoo']
#types = ['restaurant', 'cafe', 'shopping_mall', 'museum', 'gym','movie_theater','bakery', 'store', 'park', 'bowling_alley']
def makeSchedules(location, radius, maxprice, numEventsPerSchedule, numSchedules, types):
    #start = time.time()

    dictionary = []
    for i in range(0, len(types)):
        locations = nearbySearchRequestFiltered(location, radius, maxprice, types[i])
        ##THIS METHOD IS TAKING WAY TOO LONG ^^^^^
        #duration = time.time() - start
        #start = time.time()
        #logging.info("nearbySearchRequestFiltered just took " +str(duration) + " seconds to run!")
        dictionary.append(locations)
    #logging.info(dictionary)

    #markerA = time.time()
    #logging.info("MARKER A RUNTIME = " + str(markerA - start))

    schedules = []
    for index in range(numSchedules):
        schedule = ""
        for event in range(numEventsPerSchedule):
            typeIndex = random.randint(0,len(types)-1)
            while len(dictionary[typeIndex]) == 0:
                typeIndex = random.randint(0,len(types)-1)
            data = getDictionary(str(dictionary[typeIndex]))
            schedule +=  str(random.choice(data)) + "||"
        schedules.append(schedule[0:-2])

    #markerB = time.time()
    #logging.info("MARKER B RUNTIME = " + str(markerB - markerA))


    output = []
    for item in schedules:
        #logging.info(item)
        #for item2 in item.split("||"):
            #logging.info(item2)
        #    output.append(item2)
        output.append(item)

    #markerC = time.time()
    #logging.info("MARKER C RUNTIME = " + str(markerC - markerB))
    return output

def getDictionary(inputString):
    #dictionary = {}
    #logging.info(inputString)
    dictionary = yaml.load(inputString)
    return dictionary
