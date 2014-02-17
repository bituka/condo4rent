import webapp2
from google.appengine.api import mail

class Co(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('test')

app = webapp2.WSGIApplication([('/co', Co), ],
                                debug=True)