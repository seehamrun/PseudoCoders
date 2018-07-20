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

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class FavoritesHandler(webapp2.RequestHandler):
    def get(self):
        pass

class GalleryHandler(webapp2.RequestHandler):
    def get(self):
        pass

class MapHandler(webapp2.RequestHandler):
    def get(self):
        pass

class PostHandler(webapp2.RequestHandler):
    def get(self):
        pass

class ResultsHandler(webapp2.RequestHandler):
    def get(self):
        pass

class SearchHandler(webapp2.RequestHandler):
    def get(self):
        pass

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        pass

class MainHandler(webapp2.RequestHandler):
    def get(self):
        pass

app = webapp2.WSGIApplication([
    ('/favorites.html', FavoritesHandler),
    ('/gallery.html', GalleryHandler),
    ('/map.html', MapHandler),
    ('/post.html', PostHandler),
    ('/results.html', ResultsHandler),
    ('/search.html', SearchHandler),
    ('/about.html', AboutHandler),
    ('/', MainHandler)
], debug=True)
