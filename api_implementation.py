import api
import JSON
from google.app import urlFetch


# //-----------------------------------------------------------------------------//
#
#
# //SECTION 0: All places have place ID's so this function maps them to details
#
# //this function inputs a place ID
# //outputs/logs a JSON menu with place details/data
# function fetchPlaceDetails(placeID) {
#  var google_url = "https://cors.io/?" + "https://maps.googleapis.com/maps/api/place/details/"
#                  + "json" + "?"
#                  + "key=" + api_key
#                  + "&placeid=" + placeID //assembles the proper url
#   jQuery.get(google_url, (data) => {
#     //runs jQuery to fetch data and waits for completion
#     var info = fetchPlaceDetailsHelper(data)
#     //stores results from JSON menu in info variable
#     console.log(info)
#     //logs info
#   })
# }
#
# //helper function similar to the one above
# function fetchPlaceDetailsHelper(strjson) {
#   json = JSON.parse(strjson)
#   //turns string JSON into real JSON
#   return json["result"]
#   //returns the correct element from the JSON, i.e., results
# }
#
#
# //-----------------------------------------------------------------------------//
#
#
# //SECTION 1: Find Place Requests
#
# //this function inputs a search query
# //using jQuery, it fetches a JSON menu (in string form) containing the placeID associated with the query
# //it then triggers the next method fetchPlaceDetails to run
#  function findPlaceRequest(query) {
#   var google_url = "https://cors.io/?" + "https://maps.googleapis.com/maps/api/place/findplacefromtext/"
#                   + "json" + "?"
#                   + "key=" + api_key
#                   + "&input=" + query
#                   + "&inputtype=textquery" //assembles the proper url
#   jQuery.get(google_url, (data) => {
#     //runs jQuery to fetch data and waits for completion
#     var id = findPlaceRequestHelper(data)
#     //stores ID from JSON menu in id variable
#             //console.log(id)
#             //logs ID//
#     fetchPlaceDetails(id)
#     //triggers place detail fetch with this id
#   })
#  }
#
# //this function inputs a JSON menu in string form
# turns into JSON menu and outputs contents
# function findPlaceRequestHelper(strjson) {
#   json = JSON.parse(strjson)
#   //turns string JSON into real JSON
#   return json["candidates"][0]["place_id"]
#   //returns the correct element from the JSON, i.e., placeID
# }
#
#
# // //function call / TEST
# // var test_query1 = "Chicago+McDonalds";
# // findPlaceRequest(test_query1)
#
# //-----------------------------------------------------------------------------//
#
#
# //SECTION 2: Nearby Search requests
#
# //note that this requires latitude/longitude
# //this can be computed from other parts of the Google API
# //such as the Find Place Request above in Section 1
# //in that a text location/address is searched as a single location
#
#
# //this function inputs a search query
# //using jQuery, it fetches a JSON menu (in string form) containing the placeID associated with the query
# //it then triggers the next method fetchPlaceDetails to run
#  function nearbySearchRequest(location, radius) {
#   var google_url = "https://cors.io/?" + "https://maps.googleapis.com/maps/api/place/nearbysearch/"
#                   + "json" + "?"
#                   + "key=" + api_key
#                   + "&location=" + location
#                   + "&radius=" + radius //assembles the proper url
#       console.log(google_url)
#   jQuery.get(google_url, (data) => {
#     //runs jQuery to fetch data and waits for completion
#     console.log(data)
#     //triggers place detail fetch with this id
#   })
#  }
#
# // //this function inputs a JSON menu in string form
# turns into JSON menu and outputs placeID value
# // function placeIDhelper(strjson) {
# //   json = JSON.parse(strjson)
# //   //turns string JSON into real JSON
# //   return json["candidates"][0]["place_id"]
# //   //returns the correct element from the JSON, i.e., placeID
# // }
#
# //function call / TEST
# var latitude = 41.887246
# var longitude = -87.652645
# var queryLocation = latitude + "," + longitude;
# var queryRadius = 2000
# nearbySearchRequest(queryLocation, queryRadius)
#
# //-----------------------------------------------------------------------------//
#
# //SECTION 3: Text Search requests
# //not sure if this is that important, but worth checking out for sure!
