import webapp2
import jinja2
import os
import cgi
import datetime
import urllib
import sys

#contollers
class MainPage(webapp2.RequestHandler):

    def get(self):
        pass

application = webapp2.WSGIApplication([
    ('/mail', MainPage)
], debug=True)
