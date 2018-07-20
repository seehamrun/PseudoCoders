from google.appengine.ext import ndb

class Event(ndb.Model):
    name = ndb.StringProperty()
    location = ndb.StringProperty()
    date = ndb.DateProperty(auto_now_add=True)
    time = ndb.TimeProperty(auto_now_add=True)
    user_rating = ndb.IntegerProperty()
    price_level = ndb.IntegerProperty()


class Schedule(ndb.Model):
    events = ndb.StructuredProperty(Event, repeated=True)
