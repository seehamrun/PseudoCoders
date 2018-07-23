from google.appengine.ext import ndb

class LastSearchQuery(ndb.Model):
    budget = ndb.StringProperty()
    rating = ndb.StringProperty()
    userID = ndb.StringProperty()
    location = ndb.StringProperty()
    radius = ndb.StringProperty()
    date = ndb.StringProperty()
    # budget = ndb.IntegerProperty()
    # rating = ndb.IntegerProperty()
    #this will be useful later, maybe?

class Event(ndb.Model):
    name = ndb.StringProperty()
    location = ndb.StringProperty()
    date = ndb.DateProperty(auto_now_add=True)
    time = ndb.TimeProperty(auto_now_add=True)
    user_rating = ndb.IntegerProperty()
    price_level = ndb.IntegerProperty()

class Schedule(ndb.Model): #for now, this will be a single-day schedule
    events = ndb.StructuredProperty(Event, repeated=True)
    ID = ndb.IntegerProperty() #this will help us communicate with client quickly
    usersWhoSaved = ndb.StringProperty(repeated=True)

class GalleryPost(ndb.Model):
    schedule = ndb.StructuredProperty(Schedule, repeated=False)
    ID = ndb.IntegerProperty()
    description = ndb.StringProperty()
    rating = ndb.IntegerProperty()
    title = ndb.StringProperty()
    poster = ndb.StringProperty() #this will be their email
