import webapp2
import jinja2
import os
import datetime
import random
# import cgi
# import urllib
import sys
from datetime import datetime
from google.appengine.ext import db
from google.appengine.api import users
import pprint

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
	deposit = db.FloatProperty()
	
class Balance(db.Model):
	ttype = db.StringProperty(required=True, default='Income')
	amt = db.FloatProperty(required=True, default=0.0)
	description = db.StringProperty()
	notes = db.StringProperty()
	date_created = db.DateTimeProperty(auto_now_add=True)
	transaction_date = db.DateProperty()

class TotalIncome(db.Model):
	totalincomeamt = db.FloatProperty(default=0.0)
	
class TotalExpense(db.Model):
	totalexpenseamt = db.FloatProperty(default=0.0)
	
	
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
		
		user = users.get_current_user()
		
		if (user and user.nickname() == 'makaticondo4rent'):
		  
			utilitiescomputation = UtilitiesComputation()
			utilitiescomputation.tenant_name = self.request.get('tenant_name')
			utilitiescomputation.checkin_elec = float(self.request.get('checkin_elec'))
			utilitiescomputation.checkin_water = float(self.request.get('checkin_water'))
			utilitiescomputation.checkout_elec = float(self.request.get('checkout_elec'))
			utilitiescomputation.checkout_water = float(self.request.get('checkout_water'))
			utilitiescomputation.deposit = float(self.request.get('deposit'))
			
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

		else:
			self.redirect(users.create_login_url(self.request.uri))

#display latest added computation after adding entry
class LatestUtilityEntry(webapp2.RequestHandler):

	def get(self):

		user = users.get_current_user()

		if (user and user.nickname() == 'makaticondo4rent'):
			#cpu means charge per unit
			elec_cpu = 12
			water_cpu = 18

			utilitiescomputation = db.get(self.request.get('id'))
			
			elec_consume = utilitiescomputation.checkout_elec - utilitiescomputation.checkin_elec
			water_consume = utilitiescomputation.checkout_water - utilitiescomputation.checkin_water

			elec_charge = elec_consume * elec_cpu
			water_charge = water_cpu * water_consume

			total_utilities_charge = round(elec_charge + water_charge, 2)
			refund = utilitiescomputation.deposit - total_utilities_charge

			template_values = {
				'elec_consume' : elec_consume,
				'water_consume' : water_consume,
				'utilitiescomputation': utilitiescomputation,
				'water_charge' : water_charge,
				'elec_charge' : elec_charge,
				'elec_cpu' : elec_cpu,
				'water_cpu' : water_cpu,
				'total_utilities_charge' : total_utilities_charge,
				'refund' : refund
			}
			
			template = jinja_environment.get_template('company/latestutilityentry_added.html')
			self.response.out.write(template.render(template_values))
		else:
			self.redirect(users.create_login_url(self.request.uri))

#display balance for ate dhanna
#TODO
class BalancePage(webapp2.RequestHandler):
	
	def get(self):
		
		balances = db.GqlQuery("SELECT * FROM Balance ORDER BY date_created DESC LIMIT 30")
		
		q = db.Query(TotalExpense)
		totalexpense = q.get()
		
		q = db.Query(TotalIncome)
		totalincome = q.get()
		
		balanceamt = totalincome.totalincomeamt - totalexpense.totalexpenseamt
    
		template_values = {
			'balances': balances,
			'totalexpense': totalexpense.totalexpenseamt,
			'totalincome': totalincome.totalincomeamt,
			'balanceamt' : balanceamt
		}
		
		template = jinja_environment.get_template('company/balance.html')
		self.response.out.write(template.render(template_values))

class AddBalancePage(webapp2.RequestHandler):
	  
	def get(self):
	  
		user = users.get_current_user()
		
		if (user and (user.nickname() == 'makaticondo4rent' or user.nickname() == 'goryo.webdev')):
		
			template_values = {

			}

			template = jinja_environment.get_template('company/addbalance.html')
			self.response.out.write(template.render(template_values))
		
		else:
			self.redirect(users.create_login_url(self.request.uri))
  
	def post(self):
		user = users.get_current_user()
		
		if (user and (user.nickname() == 'makaticondo4rent' or user.nickname() == 'goryo.webdev')):
    		  
			# add entry to Balance Table
			balance = Balance()
			balance.ttype = str(self.request.get('type'))
			balance.amt = float(self.request.get('amt'))
			balance.description = self.request.get('description')
			balance.notes = self.request.get('notes')
			balance.transaction_date = datetime.strptime(self.request.get('transaction_date'), '%Y-%m-%d').date()
			balance.put()
			
			# add Update or Add up to the Total Income or Expense
			if (balance.ttype == 'Income'):

				q = db.Query(TotalIncome)
				totalincome = q.get()
		  
				if not totalincome:
					totalincome = TotalIncome()
					totalincome.totalincomeamt = float(balance.amt)
					totalincome.put()

					#inserted
					#self.response.out.write(totalincome.totalincomeamt)
					self.response.out.write('Added! <a href="/addbalance">Add more?</a> or <a href="/balance">Check balance</a>')
				else:
					#update existing
					totalincome.totalincomeamt += float(balance.amt)
					totalincome.put()

					self.response.out.write('Added! <a href="/addbalance">Add more?</a> or <a href="/balance">Check balance</a>')
  			 
			 
			 
			if (balance.ttype == 'Expense'):
				
				q = db.Query(TotalExpense)
				totalexpense = q.get()
		  
				if not totalexpense:
					totalexpense = TotalExpense()
					totalexpense.totalexpenseamt = float(balance.amt)
					totalexpense.put()

				else:
					#update existing
					totalexpense.totalexpenseamt += float(balance.amt)
					totalexpense.put()

				self.response.out.write('Added! <a href="/addbalance">Add more?</a> or <a href="/balance">Check balance</a>')
		else:
			self.redirect(users.create_login_url(self.request.uri))

class AdminPage(webapp2.RequestHandler):
	  
	def get(self):
	  
		user = users.get_current_user()
		
		if (user and (user.nickname() == 'makaticondo4rent' or user.nickname() == 'goryo.webdev')):
		
			
			balances = db.GqlQuery("SELECT * FROM Balance ORDER BY date_created DESC LIMIT 30")
		
			q = db.Query(TotalExpense)
			totalexpense = q.get()
			
			q = db.Query(TotalIncome)
			totalincome = q.get()
			
			balanceamt = totalincome.totalincomeamt - totalexpense.totalexpenseamt
		
			template_values = {
				'balances': balances,
				'totalexpense': totalexpense.totalexpenseamt,
				'totalincome': totalincome.totalincomeamt,
				'balanceamt' : balanceamt
			}
			
			template = jinja_environment.get_template('company/admin.html')
			self.response.out.write(template.render(template_values))
			
		
		else:
			self.redirect(users.create_login_url(self.request.uri))
  
	def post(self):
		user = users.get_current_user()
		
		if (user and (user.nickname() == 'makaticondo4rent' or user.nickname() == 'goryo.webdev')):
    		  
			# add entry to Balance Table
			balance = Balance()
			balance.ttype = str(self.request.get('type'))
			balance.amt = float(self.request.get('amt'))
			balance.description = self.request.get('description')
			balance.notes = self.request.get('notes')
			balance.transaction_date = datetime.strptime(self.request.get('transaction_date'), '%Y-%m-%d').date()
			balance.put()
			
			# add Update or Add up to the Total Income or Expense
			if (balance.ttype == 'Income'):

				q = db.Query(TotalIncome)
				totalincome = q.get()
		  
				if not totalincome:
					totalincome = TotalIncome()
					totalincome.totalincomeamt = float(balance.amt)
					totalincome.put()

					#inserted
					#self.response.out.write(totalincome.totalincomeamt)
					self.response.out.write('Added! <a href="/addbalance">Add more?</a> or <a href="/balance">Check balance</a>')
				else:
					#update existing
					totalincome.totalincomeamt += float(balance.amt)
					totalincome.put()

					self.response.out.write('Added! <a href="/addbalance">Add more?</a> or <a href="/balance">Check balance</a>')
  			 
			 
			 
			if (balance.ttype == 'Expense'):
				
				q = db.Query(TotalExpense)
				totalexpense = q.get()
		  
				if not totalexpense:
					totalexpense = TotalExpense()
					totalexpense.totalexpenseamt = float(balance.amt)
					totalexpense.put()

					#inserted
					
					self.response.out.write('Added! <a href="/addbalance">Add more?</a> or <a href="/balance">Check balance</a>')
				#	self.redirect('/addbalance', utilitiescomputation.key().id())
				else:
					#update existing
					totalexpense.totalexpenseamt += float(balance.amt)
					totalexpense.put()

					self.response.out.write('Added! <a href="/addbalance">Add more?</a> or <a href="/balance">Check balance</a>')
		else:
			self.redirect(users.create_login_url(self.request.uri))			
			
class DeleteBalanceEntry(webapp2.RequestHandler):

    def get(self):
		
		balanceentry = db.get(self.request.get('id'))
		
		# self.response.out.write(balanceentry.amt)
		
		if (balanceentry.ttype == 'Income'):
		
			q = db.Query(TotalIncome)
			totalincome = q.get()
			
			totalincome.totalincomeamt -= float(balanceentry.amt)
			totalincome.put()
			
		if (balanceentry.ttype == 'Expense'):
		
			q = db.Query(TotalExpense)
			totalexpense = q.get()
			
			totalexpense.totalexpenseamt -= float(balanceentry.amt)
			totalexpense.put()
			
		balanceentry.delete()
		self.redirect('/admin')         
		
		

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/latestutilityentry', LatestUtilityEntry),
	('/utilitiescomputation', UtilitiesComputationPage),
	('/balance', BalancePage),
	('/addbalance', AddBalancePage),
	('/deletebalanceentry', DeleteBalanceEntry),
	('/admin', AdminPage)
       
], debug=True)


