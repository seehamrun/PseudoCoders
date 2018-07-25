import webapp2
import jinja2
import os
import database
import logging
import api_implementation
import maps_api_implementation as maps
import api
import time
from google.appengine.api import users

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True) #creates environment variable for HTML rendering

class FavoritesHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template('templates/favorites.html')
        userFavoritesList = database.UserFavorites.query(database.UserFavorites.userID == users.get_current_user().user_id()).fetch()
        userFavorites = None
        if userFavoritesList == []:
            userFavorites = database.UserFavorites(userID=users.get_current_user().user_id(), favorites=[])
            userFavorites.put()
        else:
            userFavorites = userFavoritesList[0]
        newList = userFavorites.favorites #newList holds list of favoriteSchedules in Schedule forms
        list = []
        for schedule in newList: #for each Schedule object "schedule" in ^^^^
            list2 = []
            events = schedule.events #string of events
            list3 = events.split("||")
            for li in list3:
                #if len(li) > 0:
                list2.append(api_implementation.getDictionary(li))
            list.append(list2)

        data = {
            "favorites":list,
            "numEntries":len(newList)
        }
        return self.response.write(template.render(data))

class GalleryHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template('templates/gallery.html')
        return self.response.write(template.render())

class MapHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template('templates/map.html')
        # location =
        # schedule =
        map_image_url = {
            "map_image_url": "https://www.google.com/maps/embed/v1/directions?origin=+chicago,+il&waypoints=+river+forest,+il|+naperville,+il&destination=+oak+park,+il&key=%s" % (api.googleKey)
            #maps.create_map_url(location, schedule)
        }
        return self.response.write(template.render(map_image_url))

class PostHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template('templates/post.html')
        return self.response.write(template.render())

    def post(self):
        events = self.request.get('schedule')
        stored_schedule = database.Schedule(events=events) #ADD ID HERE
        stored_schedule.put()
        #not sure how exactly this will work

class SearchHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template('templates/search.html')
        return self.response.write(template.render())

        # self.response.headers['Content-Type'] = 'text/html'
        # # logging.info(budgetVar)
        # # logging.info(ratingVar)
        # response_html = jinja_env.get_template('templates/results.html')
        #
        # self.response.write(response_html.render(data))

    def post(self):

        start = time.time()

        priceVar = self.request.get('price')
        ratingVar = self.request.get('rating')
        dateVar = self.request.get('date')
        locationVar = self.request.get('location')
        radiusVar = self.request.get('radius')
        typeVar = self.request.get('type')

        markerA = time.time()
        #logging.info("MARKER A RUNTIME = " + str(markerA - start))

        userQueryItemList = database.LastSearchQuery.query(database.LastSearchQuery.userID==users.get_current_user().user_id()).fetch()
        userQueryItem = None
        if userQueryItemList == []:
            userQueryItem = database.LastSearchQuery(userID=users.get_current_user().user_id(), price=priceVar, rating=ratingVar, date=dateVar, location=locationVar, radius=radiusVar, type=typeVar)
            userQueryItem.put()
        else:
            userQueryItem = userQueryItemList[0]

        markerB = time.time()
        #logging.info("MARKER B RUNTIME = " + str(markerB - markerA))

        userQueryItem.price = priceVar
        userQueryItem.rating = ratingVar
        userQueryItem.date = dateVar
        userQueryItem.location = locationVar
        userQueryItem.radius = radiusVar
        userQueryItem.type = typeVar
        userQueryItem.put()

        markerC = time.time()
        #logging.info("MARKER C RUNTIME = " + str(markerC - markerB))

        types = []


        if typeVar == "food":
            types = ['restaurant', 'cafe', 'bakery']
        elif typeVar == "friends":
            types = ['shopping_mall', 'movie_theater', 'park', 'bowling_alley']
        elif typeVar == "diverse":
            types = ['museum', 'gym', 'store']

        markerD = time.time()
        #logging.info("MARKER D RUNTIME = " + str(markerD - markerC))


        #types = ['restaurant', 'cafe', 'shopping_mall', 'museum', 'gym','movie_theater','bakery', 'store', 'park', 'bowling_alley']
        output = api_implementation.makeSchedules(locationVar, radiusVar, priceVar, 3, 5, types)
        #assume this is a list (of schedules -> lists (of events -> strings) combined with "||")

        markerE = time.time()
        logging.info("MARKER E RUNTIME = " + str(markerE - markerD))

        userResultsItemList = database.LastResultSchedules.query(database.LastSearchQuery.userID==users.get_current_user().user_id()).fetch()

        markerF = time.time()
        #logging.info("MARKER F RUNTIME = " + str(markerF - markerE))

        userResultsItem = None
        if userResultsItemList == []:
            userResultsItem = database.LastResultSchedules(userID=users.get_current_user().user_id(), schedules=[], current=0)
            userResultsItem.put()
        else:
            userResultsItem = userResultsItemList[0]

        markerG = time.time()
        #logging.info("MARKER G RUNTIME = " + str(markerG - markerF))

        userResultsItem.schedules = []
        userResultsItem.current = 0
        userResultsItem.put()
        for schedule in output: #schedule is a list of strings combined with "||"
            #logging.info(schedule)
            newSchedule = database.Schedule(events=schedule)
            newSchedule.put()
            userResultsItem.schedules.append(newSchedule)
            userResultsItem.put()

        markerH = time.time()
        #logging.info("MARKER H RUNTIME = " + str(markerH - markerG))

        userResultsItem.put()

        #logging.info(output)
        #logging.info(len(userResultsItem.schedules))

        end = time.time()
        #logging.info("MARKER END RUNTIME = " + str(end - markerH))
        logging.info("Runtime of the Search Handler POST method is " + str(end - start) + " seconds")

        return webapp2.redirect('/results')

class ResultsHandler(webapp2.RequestHandler):
    def get(self):
        userQueryItemList = database.LastSearchQuery.query(database.LastSearchQuery.userID==users.get_current_user().user_id()).fetch()
        userQueryItem = None
        if userQueryItemList == []:
            userQueryItem = database.LastSearchQuery(price="", rating="", location="", radius="", date="", type="", userID=users.get_current_user().user_id())
            userQueryItem.put()
        else:
            userQueryItem = userQueryItemList[0]

        location = userQueryItem.location
        radius = userQueryItem.radius
        type = userQueryItem.type
        rating = userQueryItem.rating
        price = userQueryItem.price
        userID = userQueryItem.userID
        date = userQueryItem.date

        userResultsItemList = database.LastResultSchedules.query(database.LastResultSchedules.userID==users.get_current_user().user_id()).fetch()
        userResultsItem = None
        if userResultsItemList == []:
            userResultsItem = database.LastResultSchedules(schedules=[], userID=users.get_current_user().user_id(), current=0)
            userResultsItem.put()
        else:
            userResultsItem = userResultsItemList[0]
            #logging.info("WE RETRIEVED THE DATA AND DID SOMETHING WITH IT!!!!")

        #userResultsItem is a datastore schedule object with field schedules as a list of schedules
        logging.info(len(userResultsItem.schedules))
        newList = []
        if not len(userResultsItem.schedules) == 0:
            newList = userResultsItem.schedules[userResultsItem.current].events.split("||")
        #newList holds the current schedule from UserResults which is then split to become a list of events in string dictionary form

        newList2 = []
        for item in newList:
            # if len(item) > 0:
            logging.info(item)
            newList2.append(api_implementation.getDictionary(item))

        data = {
            "queryObject" : userQueryItem,
            "results" : newList2
        }

        self.response.headers['Content-Type'] = 'text/html'
        responseHTML = jinja_env.get_template('templates/results.html')
        self.response.write(responseHTML.render(data))
        #logging.info(data)

        userResultsItem.current += 1
        if userResultsItem.current >= len(userResultsItem.schedules):
            userResultsItem.current = 0
        userResultsItem.put()

    def post(self):
        #logging.info("")
        userResultsItem = database.LastResultSchedules.query(database.LastResultSchedules.userID==users.get_current_user().user_id()).fetch()[0]
        userProfile = database.UserFavorites.query(database.UserFavorites.userID==users.get_current_user().user_id()).fetch()

        if userProfile == [] or userProfile == None:
            userProfile = database.UserFavorites(userID=users.get_current_user().user_id(), favorites=[])

        if len(userResultsItem.schedules) == 0:
            logging.info("NOTHING CAN BE DONE")
        elif userResultsItem.current == 0:
            userProfile[0].favorites.append(userResultsItem.schedules[len(userResultsItem.schedules)-1])
        else:
            userProfile[0].favorites.append(userResultsItem.schedules[userResultsItem.current-1])
        userProfile[0].put()

        # if userResultsItem.current == len(userResultsItem.schedules)-1:
        #     userResultsItem.current = 0
        # else:
        #     userResultsItem.current += 1

        return webapp2.redirect('/results')


class AboutHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template('templates/about.html')
        return self.response.write(template.render())

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template('templates/main.html')
        self.response.write(template.render())
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            greeting = 'Welcome, {}! <a href="{}">sign out</a>'.format(nickname, logout_url)
        else:
            login_url = users.create_login_url('/')
            greeting = '<a href="{}">Sign in</a>'.format(login_url)

        self.response.write('<html><body><div id="login_text">{}</div></body></html>'.format(greeting))


class MaterialTestHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template('templates/material.html')
        return self.response.write(template.render())

class MaterialSearchTestHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template('templates/materialsearch.html')
        return self.response.write(template.render())

class TestHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template('templates/test.html')
        return self.response.write(template.render())

    def post(self):
        # #THIS IS A TEST OF THE fetchPlaceDetails FUNCTION:
        # self.response.headers['Content-Type'] = 'text/html'
        # placeID = self.request.get("placeID")
        # json = api_implementation.fetchPlaceDetails(placeID)
        # newList = [json]
        # data = {
        #     "results":newList
        # }
        # responseHTML = jinja_env.get_template('templates/test.html')
        # self.response.write(responseHTML.render(data))



        # #THIS IS A TEST OF THE findPlaceRequest FUNCTION:
        # self.response.headers['Content-Type'] = 'text/html'
        # query = self.request.get("query")
        # json = api_implementation.findPlaceRequest(query)
        # newList = json
        # data = {
        #     "results":newList
        # }
        # responseHTML = jinja_env.get_template('templates/test.html')
        # self.response.write(responseHTML.render(data))


        # #THIS IS A TEST OF THE getFields FUNCTION:
        # self.response.headers['Content-Type'] = 'text/html'
        # output = api_implementation.getFields()
        # newList = [output]
        # data = {
        #     "results":newList
        # }
        # responseHTML = jinja_env.get_template('templates/test.html')
        # self.response.write(responseHTML.render(data))


        # #THIS IS A TEST OF THE getLatitudeLongitude FUNCTION:
        # self.response.headers['Content-Type'] = 'text/html'
        # location = self.request.get("location")
        # output = api_implementation.getLatitudeLongitude(location)
        # newList = [output]
        # data = {
        #     "results":newList
        # }
        # responseHTML = jinja_env.get_template('templates/test.html')
        # self.response.write(responseHTML.render(data))


        # #THIS IS A TEST OF THE nearbySearchRequest FUNCTION:
        # self.response.headers['Content-Type'] = 'text/html'
        # location = self.request.get("location")
        # radius = self.request.get("radius")
        # json = api_implementation.nearbySearchRequest(location, radius)
        # newList = json
        # data = {
        #     "results" : newList
        # }
        # responseHTML = jinja_env.get_template('templates/test.html')
        # self.response.write(responseHTML.render(data))


        # #THIS IS A TEST OF THE nearbySearchRequestFiltered FUNCTION:
        # self.response.headers['Content-Type'] = 'text/html'
        # location = self.request.get("location")
        # radius = self.request.get("radius")
        # price = self.request.get("price")
        # type = self.request.get("type")
        # json = api_implementation.nearbySearchRequestFiltered(location, radius, price, type)
        # #json = api_implementation.nearbySearchRequest(location, radius)
        # newList = json
        # data = {
        #     "results" : newList
        # }
        # responseHTML = jinja_env.get_template('templates/test.html')
        # self.response.write(responseHTML.render(data))


        #THIS IS A TEST OF THE makeSchedules FUNCTION:
        self.response.headers['Content-Type'] = 'text/html'
        location = self.request.get("location")
        radius = self.request.get("radius")
        price = self.request.get("price")
        json = api_implementation.makeSchedules(location, radius, price)
        #json = api_implementation.nearbySearchRequest(location, radius)
        newList = json
        data = {
            "results" : newList
        }
        responseHTML = jinja_env.get_template('templates/test.html')
        self.response.write(responseHTML.render(data))


app = webapp2.WSGIApplication([
    ('/favorites', FavoritesHandler),
    ('/gallery', GalleryHandler),
    ('/map', MapHandler),
    ('/post', PostHandler),
    ('/results', ResultsHandler),
    ('/search', SearchHandler),
    ('/about', AboutHandler),
    ('/test', TestHandler),
    ('/material', MaterialTestHandler),
    ('/materialsearch', MaterialSearchTestHandler),
    ('/', MainHandler)
], debug=True)
