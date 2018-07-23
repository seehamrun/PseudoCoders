# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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


class ResultsHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        response_html = jinja_env.get_template('templates/results.html')
        data = {
            'queryObject': database.LastSearchQuery.query(database.LastSearchQuery.userID==users.get_current_user().user_id()).fetch()[0]
        }
        return self.response.write(response_html.render(data))

    def post(self):
        logging.data("")

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
        budgetVar = self.request.get('budget')
        ratingVar = self.request.get('rating')
        dateVar = self.request.get('date')
        locationVar = self.request.get('location')
        radiusVar = self.request.get('radius')
        # searchQuery = {
        #     'var_budget': budgetVar,
        #     'var_rating': ratingVar,
        #     'var_ID': 0 #later a real ID will be added here
        # }
        # template = jinja_env.get_template('templates/temp_screen.html')

        userItem = database.LastSearchQuery.query(database.LastSearchQuery.userID==users.get_current_user().user_id()).fetch()
        if userItem == []:
            newItem = database.LastSearchQuery(userID=users.get_current_user().user_id(), budget=budgetVar, rating=ratingVar, date=dateVar, location=locationVar, radius=radiusVar)
            newItem.put()
        else:
            userItem[0].budget = budgetVar
            userItem[0].rating = ratingVar
            userItem[0].date = dateVar
            userItem[0].location = locationVar
            userItem[0].radius = radiusVar
            userItem[0].put()

        logging.info(userItem)
        userItem = database.LastSearchQuery.query(database.LastSearchQuery.userID==users.get_current_user().user_id()).fetch()
        userItem[0].put()
        # lastQuery.budget = budgetVar
        # lastQuery.rating = ratingVar
         #lastQuery.put()

        #return self.response.write(template.render(searchQuery))
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
        return self.response.write(template.render())

        # user = users.get_current_user()
        # logging.info('current user is %s' % (user.nickname()))
        # template = jinja_env.get_template('templates/main.html')
        # data = {
        #   'user_name': user.name(),
        #   'logout_url': users.create_logout_url('/')
        # }
        # return self.response.write(template.render(data))

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template('templates/welcome.html')
        return self.response.write(template.render())

class TestHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = jinja_env.get_template('templates/test.html')
        return self.response.write(template.render())

    def post(self):
        placeID = self.request.get("placeID")
        self.response.headers['Content-Type'] = 'text/html'
        json = api_implementation.fetchPlaceDetails(placeID)
        data = {
            "results" : json
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
    ('/main', MainHandler),
    ('/', WelcomeHandler)
], debug=True)
