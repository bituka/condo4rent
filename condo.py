import webapp2
import jinja2
import os
import cgi
import datetime
import urllib
import sys

from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import users
from google.appengine.api import mail

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

#models 
class UtilitiesComputation(db.Model):
    checkin_elec = db.IntegerProperty()
    checkout_elec = db.IntegerProperty()
    checkin_water = db.IntegerProperty()
    checkout_water = db.IntegerProperty()
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
        utilitiescomputation.checkin_elec = int(self.request.get('checkin_elec'))
        utilitiescomputation.checkin_water = int(self.request.get('checkin_water'))
        utilitiescomputation.checkout_elec = int(self.request.get('checkout_elec'))
        utilitiescomputation.checkout_water = int(self.request.get('checkout_water'))
        
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

        total_utilities_charge = elec_charge + water_charge
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

class EmailUtilitiesDraft(webapp2.RequestHandler):
#    def get(self):

#         user = users.get_current_user()

#         if (user and user.nickname() == 'makaticondo4rent'):
           
#            checkin_elec = self.request.get('checkin_elec')
#            checkout_elec = self.request.get('checkout_elec')
#            checkin_water = self.request.get('checkin_elec')
#            checkout_water = self.request.get('checkout_water')
#            elec_consume  = self.request.get('elec_consume')
#            water_consume = self.request.get('water_consume')
#            elec_cpu = self.request.get('elec_cpu')
#            water_cpu = self.request.get('water_cpu')

#            template_values = {
#             'elec_consume' : elec_consume,
#             'water_consume' : water_consume,
#             'water_charge' : water_charge,  
#             'elec_charge' : elec_charge,   
#             'elec_cpu' : elec_cpu,
#             'water_cpu' : water_cpu,
#             'total_utilities_charge' : total_utilities_charge
#             }
#         else:
#             self.redirect(users.create_login_url(self.request.uri))

    def post(self):
        if (user and user.nickname() == 'makaticondo4rent'):

           checkin_elec = self.request.get('checkin_elec')
           checkout_elec = self.request.get('checkout_elec')
           checkin_water = self.request.get('checkin_elec')
           checkout_water = self.request.get('checkout_water')
           elec_consume  = self.request.get('elec_consume')
           water_consume = self.request.get('water_consume')
           elec_cpu = self.request.get('elec_cpu')
           water_cpu = self.request.get('water_cpu')


        else:
            self.redirect(users.create_login_url(self.request.uri))

#send utilities computation to tenant
class SendUtilitiesTenant(webapp2.RequestHandler):

    def post(self):

        user = users.get_current_user()

        if (user and user.nickname() == 'makaticondo4rent'):

            checkin_elec = self.request.get('checkin_elec')
            checkout_elec = self.request.get('checkout_elec')
            checkin_water = self.request.get('checkin_elec')
            checkout_water = self.request.get('checkout_water')
            elec_consume  = self.request.get('elec_consume')
            water_consume = self.request.get('water_consume')
            elec_cpu = self.request.get('elec_cpu')
            water_cpu = self.request.get('water_cpu')
            to_email = self.request.get('to_email')

            message = mail.EmailMessage()
            message.sender = user.email()
            message.subject = "Test Mail"
            message.to = to_email
            message.html = """
                <html>
                <header><title></title></header>
                <body> %s   </body>
                </html>
                """ % checkin_elec
            message.send() 
        
        else:
            
            self.redirect(users.create_login_url(self.request.uri))

        

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/latestutilityentry', LatestUtilityEntry),
    ('/utilitiescomputation', UtilitiesComputationPage),
    ('/sendutilitiestenant', SendUtilitiesTenant),
    ('/emailutilitiesdraft', EmailUtilitiesDraft),
    
], debug=True)


