from django.db import models
from datetime import datetime, timedelta,date
from django.urls import reverse
from django.utils import timezone
from investors.models import Account
import random
import json
import uuid


class Packages(models.Model):
    name = models.CharField(max_length=50)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    percent = models.IntegerField(blank=True,null=True)

	 

    def __str__(self):
        return self.name

  



class Investment(models.Model):
	STATUS = (
		("Active","active"),
		("complete","complete"),
	)
	WITHSTATUS = (
		("pending","pending"),
		("complete","complete"),
	)
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	pack = models.ForeignKey('Packages', on_delete=models.CASCADE)
	start_date = models.DateTimeField(auto_now_add=True)
	end_date = models.DateTimeField()
	status = models.CharField(max_length=40, choices=STATUS)
	total_prof = models.IntegerField(default=0, blank=True,null=True)
	withdraw = models.BooleanField(default=False)
	primary_withdraw = models.BooleanField(default=False,blank=True,null=True)
	p_with_status = models.BooleanField(blank=True,null=True)

	class Meta:
		ordering = ['-start_date']



	@property
	def is_past_due(self):
		time = timezone.now()
		if time >= self.end_date:
			return True
		return False



	def total_earnings(self):
	    perc = self.daily()
	    total = perc * 15
	    return total

	def daily(self):
		price = self.pack.amount
		percent = 30
		perc = percent/100 * price
		return perc










	def __str__(self):
		return f"{self.user.username} invest of {self.pack.name}"



class Order(models.Model):
    user = models.ForeignKey( Account, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    investment = models.ManyToManyField(Investment, related_name='investment_order')

    def __str__(self):
        return self.user.username


    def total_invested(self):
        total_money = 0
        for obj in self.investment.all():
            total_money += obj.pack.amount
        return total_money

    def total_invesment(self):
        obj = self.investment.all().count()
        return obj





class Withdraw(models.Model):
	user = models.ForeignKey( Account, on_delete=models.CASCADE,related_name="with_user")
	investment = models.ForeignKey( Investment, on_delete=models.CASCADE, related_name="with_investment",blank=True,null=True)
	bank_name = models.CharField(max_length=50)
	account_number = models.CharField(max_length=50)
	account_name =models.CharField(max_length=50)
	amount = models.IntegerField(default=0, blank=True,null=True)
	date = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)

	class Meta:
		ordering = ['-date']

	def __str__(self):
		return f"{self.user.username} withdraw "





class ReferalWithdraw(models.Model):
	user = models.ForeignKey( Account, on_delete=models.CASCADE,related_name="ref_with_user")
	bank_name = models.CharField(max_length=50)
	account_number = models.CharField(max_length=50)
	account_name =models.CharField(max_length=50)
	amount = models.IntegerField(default=0, blank=True,null=True)
	date = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)

	class Meta:
		ordering = ['-date']

	def __str__(self):
		return f"{self.user.username} referal withdraw "


def rand_str():
      return str(random.randint(1000000000, 9999999999))

class VerificationCode(models.Model):
	name = models.CharField(max_length=50,blank=True,null=True)
	amount = models.IntegerField(blank=True,null=True)
	date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
	code = models.CharField(max_length=50)
	active = models.BooleanField(default=True)
	package = models.ForeignKey('Packages', on_delete=models.CASCADE,blank=True,null=True)

	class Meta:
		ordering = ['-date']



	def __str__(self):
		return f"{self.package.amount}"









class Message(models.Model):
	name = models.CharField(max_length=50,blank=True,null=True)
	email = models.CharField(max_length=50,blank=True,null=True)
	date = models.DateTimeField(auto_now_add=True)
	message = models.TextField()


	class Meta:
		ordering = ['-date']

	def __str__(self):
		return f"{self.name}"
