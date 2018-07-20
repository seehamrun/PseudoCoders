import webapp2
import logging
import jinja2
import os
from google.appengine.ext import ndb


class FavoriteUrl(ndb.Model):
    url = ndb.StringProperty()


jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class IndexHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        logging.info('current user is %s' % (user.nickname()))
        template = jinja_env.get_template('templates/index.html')
        data = {
          'logoutUrl': users.create_logout_url('/')
        }
        return self.response.write(template.render(data))


class AddFavoriteHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        logging.info('current user is %s' % (user.nickname()))
        requestUrl = self.request.get('url')
        logging.info('server saw a request to add %s to list of favorites' % (requestUrl))
        favoriteUrl = FavoriteUrl(url=requestUrl)
        favoriteUrl.put()


class ListFavoritesHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        logging.info('current user is %s' % (user.nickname()))
        template = jinja_env.get_template('templates/favorites.html')
        data = {
          'favorites': FavoriteUrl.query().fetch(),
          'logoutUrl': users.create_logout_url('/'),
        }
        return self.response.write(template.render(data))


app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/add_favorite', AddFavoriteHandler),
    ('/list_favorites', ListFavoritesHandler)
], debug=True)
