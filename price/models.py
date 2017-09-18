from django.contrib.auth.models import Permission, User
from django.db import models
from django.utils import timezone

class Transaction(models.Model):
	user = models.ForeignKey(User)
	transact_date = models.DateTimeField(default=timezone.now)
	virtual_cash=models.FloatField(default=0.0)
	company_symbol = models.CharField(max_length=250)
	purchase_rate = models.FloatField(default=0.0)
	purchase_quantity = models.PositiveSmallIntegerField(default=0)
	purchase_amount = models.FloatField(default=0.0)
	sale_rate = models.FloatField(default=0.0)
	sale_quantity = models.PositiveSmallIntegerField(default=0)
	sale_amount = models.FloatField(default=0.0)
	profit = models.FloatField(default=0.0)
	balance_shares=models.IntegerField(default=0)
	
	

	def __str__(self):
		return str(self.user) + ' - ' + self.company_symbol
		
class UserInfo(models.Model):
	#user=models.IntegerField(default=0)
	user = models.ForeignKey(User)
	virtual_cash=models.FloatField(default=0.0)
	
	def __str__(self):
		return str(self.user) + ' - ' + str(self.virtual_cash)
		
class Portfolio(models.Model):
	user = models.ForeignKey(User)
	c_name=models.CharField(max_length=250)
	bought_shares=models.IntegerField(default=0)
	sold_shares=models.IntegerField(default=0)
	bal_shares=models.IntegerField(default=0)
	current_market_price=models.FloatField(default=0.0)
	market_evaluation=models.FloatField(default=0.0)
	profit=models.FloatField(default=0.0)
	
	def __str__(self):
		return str(self.user) + ' - ' + str(self.profit)
	
	


