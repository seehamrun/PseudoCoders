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
    events = ndb.StringProperty(repeated=True)
    usersWhoSaved = ndb.StringProperty(repeated=True)

class LastResultSchedules(ndb.Model):
    schedules = ndb.StructuredProperty(Schedule, repeated=True)
    userID = ndb.StringProperty()

#THIS IS THE ONLY ONE WE NEED TO CHANGE
class GalleryPost(ndb.Model):
    schedule = ndb.StructuredProperty(Schedule, repeated=False)
    ID = ndb.IntegerProperty()
    description = ndb.StringProperty()
    rating = ndb.IntegerProperty()
    title = ndb.StringProperty()
    poster = ndb.StringProperty() #this will be their email
