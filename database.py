from google.appengine.ext import ndb

class LastSearchQuery(ndb.Model):
    price = ndb.StringProperty()
    rating = ndb.StringProperty()
    location = ndb.StringProperty()
    radius = ndb.StringProperty()
    date = ndb.StringProperty()
    userID = ndb.StringProperty()
    type = ndb.StringProperty()
    # budget = ndb.IntegerProperty()
    # rating = ndb.IntegerProperty()
    #this will be useful later, maybe?

class Schedule(ndb.Model): #for now, this will be a single-day schedule
    events = ndb.StringProperty()
    # usersWhoSaved = ndb.StringProperty()
    #this will have to be a list in String form

class UserFavorites(ndb.Model):
    userID = ndb.StringProperty()
    favorites = ndb.StructuredProperty(Schedule, repeated=True)
    current = ndb.IntegerProperty()

class LastResultSchedules(ndb.Model):
    schedules = ndb.StructuredProperty(Schedule, repeated=True)
    userID = ndb.StringProperty()
    current = ndb.IntegerProperty()

#THIS IS THE ONLY ONE WE NEED TO CHANGE
class GalleryPost(ndb.Model):
    schedule = ndb.StructuredProperty(Schedule, repeated=False)
    #ID = ndb.IntegerProperty()
    description = ndb.StringProperty()
    rating = ndb.IntegerProperty()
    title = ndb.StringProperty()
    poster = ndb.StringProperty() #this will be their ID
