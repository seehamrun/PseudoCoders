var api_key = "HIDDEN";
var test_query = "Chicago+McDonalds";
//this is a test query that I’m using -> feel free to change

//this function inputs a search query
//using jQuery, it fetches a JSON menu (in string form) containing the placeID associated with the query
//it then triggers the next method fetchPlaceDetails to run
 function fetchPlaceID(query) {
  var google_url = "https://cors.io/?" + "https://maps.googleapis.com/maps/api/place/findplacefromtext/"
                  + "json" + "?"
                  + "key=" + api_key
                  + "&input=" + test_query
                  + "&inputtype=textquery" //assembles the proper url
  jQuery.get(google_url, (data) => {
    //runs jQuery to fetch data and waits for completion
    var id = placeIDhelper(data)
    //stores ID from JSON menu in id variable
            /*console.log(id)
            //logs ID*/
    fetchPlaceDetails(id)
    //triggers place detail fetch with this id
  })
 }

//this function inputs a JSON menu in string form
//turns it into an actual json menu and then outputs the menu’s placeID value
function placeIDhelper(strjson) {
  json = JSON.parse(strjson)
  //turns string JSON into real JSON
  return json["candidates"][0]["place_id"]
  //returns the correct element from the JSON, i.e., placeID
}

//this function inputs a place ID
//outputs/logs a JSON menu with place details/data
function fetchPlaceDetails(placeID) {
 var google_url = "https://cors.io/?" + "https://maps.googleapis.com/maps/api/place/details/"
                 + "json" + "?"
                 + "key=" + api_key
                 + "&placeid=" + placeID //assembles the proper url
  jQuery.get(google_url, (data) => {
    //runs jQuery to fetch data and waits for completion
    var info = placeDetailsHelper(data)
    //stores results from JSON menu in info variable
    console.log(info)
    //logs info
  })
}

//helper function similar to the one above
function placeDetailsHelper(strjson) {
  json = JSON.parse(strjson)
  //turns string JSON into real JSON
  return json["result"]
  //returns the correct element from the JSON, i.e., results
}

//function call
fetchPlaceID(test_query)
