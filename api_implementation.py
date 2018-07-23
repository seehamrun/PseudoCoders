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

def fetchNameAddress(placeID):
    info = fetchPlaceDetails(placeID)
<<<<<<< HEAD
    return info['name']+" ---> "+info['formatted_address']
=======
    return info#['candidates']
>>>>>>> 5bdb09e4c14cdada15df1de2b764a0a0d93b14b1

#inputs search query and returns result data
def findPlaceRequest(query):
    id = findPlaceRequestHelper(query)
    return fetchPlaceDetails(id)

#inputs search query and returns any amount of data, in this case only result ID
def findPlaceRequestHelper(query):
    newQuery = query.replace(" ", "+")
    google_url = "https://cors.io/?" + "https://maps.googleapis.com/maps/api/place/findplacefromtext/%s?input=%s&inputtype=textquery&key=%s&fields=%s" % ("json", newQuery, api.googleKey, getFields())
    urlContent = urlfetch.fetch(google_url).content
    response = json.loads(urlContent)
    return response['candidates'][0]['place_id']

#sets the fields returned by helper above, only necessary field is place ID
def getFields():
    output = ""
    #output += "name,"
    #output += "formatted_address,"
    #output += "geometry,"
    #output += "icon,"
    #output += "id,"
    #output += "name,"
    #output += "permanently_closed,"
    #output += "photos,"
    output += "place_id,"
    #output += "plus_code,"
    #output += "scope,"
    #output += "types,"
    #output += "opening_hours,"
    #output += "price_level,"
    #output += "rating,"
    return output[:-1]


#takes latitude/longitude -> can be computed from other Google API
#also inputs a search query
def nearbySearchRequest(location, radius):
    google_url = "https://cors.io/?" + "https://maps.googleapis.com/maps/api/place/nearbysearch/%s?key=%s&location=%s&radius=%s" % ("json", api.googleKey, getLatitudeLongitude(location), radius)
    urlContent = urlfetch.fetch(google_url).content
    response = json.loads(urlContent)
    #return response
    list = []
    for item in response["results"]:
        list.append(item["place_id"])
    return list


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
#       console.log(google_url)
#   jQuery.get(google_url, (data) => {
#     #runs jQuery to fetch data and waits for completion
#     console.log(data)
#     #triggers place detail fetch with this id
#   })
#  }
#
# # #this function inputs a JSON menu in string form
# turns into JSON menu and outputs placeID value
# # function placeIDhelper(strjson) {
# #   json = JSON.parse(strjson)
# #   #returns string JSON into real JSON
# #   return json["candidates"][0]["place_id"]
# #  #returns the correct element from the JSON, i.e., placeID
# # }
#
# #function call / TEST
# var latitude = 41.887246
# var longitude = -87.652645
# var queryLocation = latitude + "," + longitude;
# var queryRadius = 2000
# nearbySearchRequest(queryLocation, queryRadius)
#
# #-----------------------------------------------------------------------------//
#
# #SECTION 3: Text Search requests
# #not sure if this is that important, but worth checking out for sure!
