import webapp2
from google.appengine.api import mail
from google.appengine.api import users

class CondoMail(webapp2.RequestHandler):

    def get(self):

        pass

    def post(self):

        user = users.get_current_user()

        if (user and user.nickname() == 'makaticondo4rent'):

            tenant_name = self.request.get('tenant_name')
            checkin_elec = self.request.get('checkin_elec')
            checkout_elec = self.request.get('checkout_elec')
            checkin_water = self.request.get('checkin_water')
            checkout_water = self.request.get('checkout_water')
            elec_consume  = self.request.get('elec_consume')
            water_consume = self.request.get('water_consume')
            elec_cpu = self.request.get('elec_cpu')
            water_cpu = self.request.get('water_cpu')
            to_email = self.request.get('to_email')
            elec_charge = self.request.get('elec_charge')
            water_charge = self.request.get('water_charge')
            total_utilities_charge = self.request.get('total_utilities_charge')
            deposit = self.request.get('deposit')
            refund = self.request.get('refund')

            message = mail.EmailMessage()
            message.sender = user.email()
            message.subject = "Utilities Computation from Condo4Rent"
            message.to = to_email
            message.body = """
Dear %s,

Thank you choosing us again on your stay. Below are the readings and computation of your utilities consumed. 

Electric: 
Checkin = %s
Checkout = %s
Consumed Electricity = %s

Water:
Checkin = %s
Checkout        = %s
Consumed Water = %s

Charges: 
Electricity Charge(Charge per Unit = %s PHP): %s PHP
Water Charge(Charge per Unit = %s PHP): %s PHP
Total Utilities Charge = %s
Deposit: %s
Refund: %s


            """ % (tenant_name, checkin_elec, checkout_elec, elec_consume, checkin_water, checkout_water, 
                water_consume, elec_cpu, elec_charge, water_cpu, water_charge, 
                total_utilities_charge, deposit, refund)
            # message.html = """
            #     <html>
            #     <header><title></title></header>
            #     <body> %s   </body>
            #     </html>
            #     """ % checkin_elec
            message.send() 
            self.redirect('/utilitiescomputation')
        else:
            
            self.redirect(users.create_login_url(self.request.uri))

app = webapp2.WSGIApplication([('/condomail', CondoMail), ],
                                debug=True)

