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
    return response["result"]

#inputs search query and returns JSON menu with details
def findPlaceRequest(query):
    google_url = "https://cors.io/?" + "https://maps.googleapis.com/maps/api/place/findplacefromtext/%s?input=%s&inputtype=textquery&key=%s&fields=photos,formatted_address,name,rating,opening_hours,geometry" % ("json", query, api.googleKey)
    #logging.info(query)
    logging.info(google_url)
    urlContent = urlfetch.fetch(google_url).content
    #logging.info("URL CONTENT:" + urlContent)
    response = json.loads(urlContent)
    return response


# #this function inputs a JSON menu in string form
# turns into JSON menu and outputs contents
# function findPlaceRequestHelper(strjson) {
#   json = JSON.parse(strjson)
#   #turns string JSON into real JSON
#   return json
#   #returns the correct element from the JSON, i.e., placeID
# }
#
#
# # #function call / TEST
# # var test_query1 = "Chicago+McDonalds";
# # findPlaceRequest(test_query1)
#
# #-----------------------------------------------------------------------------//
#
#
# #SECTION 2: Nearby Search requests
#
# #note that this requires latitude/longitude
# #this can be computed from other parts of the Google API
# #such as the Find Place Request above in Section 1
# #in that a text location/address is searched as a single location
#
#
# #this function inputs a search query
# #using jQuery, it fetches a JSON menu (in string form) containing the placeID associated with the query
# #it then triggers the next method fetchPlaceDetails to run
#  function nearbySearchRequest(location, radius) {
#   var google_url = "https://cors.io/?" + "https://maps.googleapis.com/maps/api/place/nearbysearch/"
#                   + "json" + "?"
#                   + "key=" + api_key
#                   + "&location=" + location
#                   + "&radius=" + radius //assembles the proper url
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
