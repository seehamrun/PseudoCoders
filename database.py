from google.appengine.ext import ndb

class Event(ndb.Model):
    name = ndb.StringProperty()
    location = ndb.StringProperty()
    date = ndb.DateProperty(auto_now=True)
    time = ndb.TimeProperty(auto_now=True)
    user_rating = ndb.IntegerProperty()
    price_level = ndb.IntegerProperty()


class Schedule(ndb.Model):
