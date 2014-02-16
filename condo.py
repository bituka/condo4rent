import webapp2
import jinja2
import os
# import cgi
# import datetime
# import urllib
# import sys

from google.appengine.ext import db
# from google.appengine.api import users


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

#models 
class UtilitiesComputation(db.Model):
    checkin_elec = db.FloatProperty()
    checkout_elec = db.FloatProperty()
    checkin_water = db.FloatProperty()
    checkout_water = db.FloatProperty()
    tenant_name = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    

#contollers
class MainPage(webapp2.RequestHandler):

    def get(self):
        template_values = {
            
        }
        
        template = jinja_environment.get_template('public/index.html')
        self.response.out.write(template.render(template_values))
        
class UtilitiesComputationPage(webapp2.RequestHandler):

    def get(self):
        template_values = {
            
        }
        
        template = jinja_environment.get_template('company/utilities_main.html')
        self.response.out.write(template.render(template_values))

    def post(self):   
        utilitiescomputation = UtilitiesComputation()
        utilitiescomputation.tenant_name = self.request.get('tenant_name')
        utilitiescomputation.checkin_elec = float(self.request.get('checkin_elec'))
        utilitiescomputation.checkin_water = float(self.request.get('checkin_water'))
        utilitiescomputation.checkout_elec = float(self.request.get('checkout_elec'))
        utilitiescomputation.checkout_water = float(self.request.get('checkout_water'))
        
        utilitiescomputation.put()
    #    item.key().id()

    #    redirectUrl = "/view/key/%s/" % item.key()
    #    self.redirect(redirectUrl)
    #    test = utilitiescomputation.key().id()
    #    print test 

        redirectUrl = "/latestutilityentry?id=%s" % utilitiescomputation.key()
    #    print redirectUrl        

        self.redirect(redirectUrl)
    #    self.redirect('/latestutilityentry', utilitiescomputation.key().id())            

#display latest added computation after adding entry
class LatestUtilityEntry(webapp2.RequestHandler):
    def get(self):   
        #cpu means charge per unit
        elec_cpu = 12
        water_cpu = 18

        utilitiescomputation = db.get(self.request.get('id'))
        
        elec_consume = utilitiescomputation.checkout_elec - utilitiescomputation.checkin_elec
        water_consume = utilitiescomputation.checkout_water - utilitiescomputation.checkin_water

        elec_charge = elec_consume * elec_cpu 
        water_charge = water_cpu * water_consume

        total_utilities_charge = round(elec_charge + water_charge, 2)
        template_values = {
            'elec_consume' : elec_consume,
            'water_consume' : water_consume,
            'utilitiescomputation': utilitiescomputation,
            'water_charge' : water_charge,  
            'elec_charge' : elec_charge,   
            'elec_cpu' : elec_cpu,
            'water_cpu' : water_cpu,
            'total_utilities_charge' : total_utilities_charge
        }
        
        template = jinja_environment.get_template('company/latestutilityentry_added.html')
        self.response.out.write(template.render(template_values)) 

        

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/latestutilityentry', LatestUtilityEntry),
    ('/utilitiescomputation', UtilitiesComputationPage),
    
], debug=True)


