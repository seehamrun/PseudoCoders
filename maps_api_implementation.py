import api
import json
import logging
import ast
import yaml
import re
from google.appengine.api import urlfetch

def create_map(location, schedule):
    waypoints = []
    for event in schedule:
        address = event['ADDRESS']
        waypoints.append(address)
        
    formatted_waypoints = waypoints[0]
    for waypoint in waypoints[1:]:
        formatted_waypoints += "|" + waypoint.replace(' ', '+')
    map_image_url = "https://www.google.com/maps/embed/v1/directions?key=%s&origin=%s&waypoints=%s&destination=%s" % (api.googleKey, location, formatted_waypoints, location)

    return map_image_url
