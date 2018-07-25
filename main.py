import webapp2
import jinja2
import os
import database
import logging
import api_implementation
from google.appengine.api import users

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True) #creates environment variable for HTML rendering

class FavoritesHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template('templates/favorites.html')
        return self.response.write(template.render())

class GalleryHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template('templates/gallery.html')
        return self.response.write(template.render())

class MapHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template('templates/map.html')
        return self.response.write(template.render())

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
        priceVar = self.request.get('price')
        ratingVar = self.request.get('rating')
        dateVar = self.request.get('date')
        locationVar = self.request.get('location')
        radiusVar = self.request.get('radius')
        typeVar = self.request.get('type')

        userQueryItem = database.LastSearchQuery.query(database.LastSearchQuery.userID==users.get_current_user().user_id()).fetch()
        if userQueryItem == []:
            newItem = database.LastSearchQuery(userID=users.get_current_user().user_id(), price=priceVar, rating=ratingVar, date=dateVar, location=locationVar, radius=radiusVar, type=typeVar)
            newItem.put()
        else:
            userQueryItem[0].price = priceVar
            userQueryItem[0].rating = ratingVar
            userQueryItem[0].date = dateVar
            userQueryItem[0].location = locationVar
            userQueryItem[0].radius = radiusVar
            userQueryItem[0].type = typeVar
            userQueryItem[0].put()

        #logging.info(userQueryItem)
        userQueryItem = database.LastSearchQuery.query(database.LastSearchQuery.userID==users.get_current_user().user_id()).fetch()
        userQueryItem[0].put()


        output = api_implementation.makeSchedules(locationVar, radiusVar, priceVar, 5, 10)
        #assume this is a list of lists of strings

        userResultsItem = database.LastResultSchedules.query(database.LastSearchQuery.userID==users.get_current_user().user_id()).fetch()
        if userResultsItem == []:
            generatedSchedules = []
            userResultsItem = database.LastResultSchedules(userID=users.get_current_user().user_id(), schedules=[])
            userResultsItem.put()
        else:
            userResultsItem[0].schedules = []
            userResultsItem[0].put()
        for schedule in output:
            newSchedule = database.Schedule(events=schedule, usersWhoSaved=[])
            newSchedule.put()
            newItem.schedules.append(newSchedule)
            newItem.put()

        return webapp2.redirect('/results')

class ResultsHandler(webapp2.RequestHandler):
    def get(self):
        userQueryItem = database.LastSearchQuery.query(database.LastSearchQuery.userID==users.get_current_user().user_id()).fetch()[0]
        location = userQueryItem.location
        radius = userQueryItem.radius
        type = userQueryItem.type
        rating = userQueryItem.rating
        price = userQueryItem.price
        userID = userQueryItem.userID
        date = userQueryItem.date

        userResultsItem = database.LastResultSchedules.query(database.LastResultSchedules.userID==users.get_current_user().user_id()).fetch()[0]
        newList = userResultsItem.schedules

        data = {
            "queryObject":userQueryItem,
            "results" : newList
        }

        self.response.headers['Content-Type'] = 'text/html'
        responseHTML = jinja_env.get_template('templates/results.html')
        self.response.write(responseHTML.render(data))
        #logging.info(data)

    def post(self):
        logging.data("")

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
            greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(nickname, logout_url)
        else:
            login_url = users.create_login_url('/')
            greeting = '<a href="{}">Sign in</a>'.format(login_url)

        self.response.write('<html><body>{}</body></html>'.format(greeting))


class MaterialTestHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template('templates/material.html')
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
    ('/', MainHandler)
], debug=True)
