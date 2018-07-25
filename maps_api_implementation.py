import api
import json
import logging
import ast
import random
import yaml
import re
from google.appengine.api import urlfetch

# def create_map(location, schedule):
#     waypoints = []
#     for event in schedule:
#         address = event[]
#         waypoints.append(address)
#     map_image_url = "https://www.google.com/maps/embed/v1/directions?key=%s&origin=%s&destination=%s" % (api.googleKey, location, location)
#     return map_image_url
