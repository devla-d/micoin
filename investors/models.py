
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import random
import json
import uuid

class MyAccountManager(BaseUserManager):
	def create_user(self,username, email, password=None):
		if not email:
			raise ValueError('email is required')
		if not username:
			raise ValueError('username is required')
		
		user = self.model(
			email= self.normalize_email(email),
			username= username
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username,email,password):
		user = self.create_user(
			 email= self.normalize_email(email),
			username= self.normalize_username(username),
			password= password,
		
		)
		user.is_admin=True
		user.is_superuser=True
		user.is_staff= True
		user.save(using=self._db)
		return user





def rand_str():
	  return str(random.randint(100, 999))


class Account(AbstractBaseUser):
	email       = models.EmailField(verbose_name='email', max_length=60, unique=True )
	username    = models.CharField(max_length=30, unique=True)
	date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login  = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin    = models.BooleanField(default=False)
	is_staff    = models.BooleanField(default=False)
	is_active   = models.BooleanField(default=True)
	is_superuser = models.BooleanField(default=False)
	profile_image = models.ImageField(blank=True, null=True, default='default.jgp', upload_to='profile')
	phone = models.CharField(max_length=30, blank=True,null=True,unique=True)
	refferal = models.IntegerField(default=0, blank=True,null=True)
	balance = models.IntegerField(default=0, blank=True,null=True)
	referral_balance = models.IntegerField(default=0, blank=True,null=True)
	withdraw_total = models.IntegerField(default=0, blank=True,null=True)
	investment_earnings = models.IntegerField(default=0, blank=True,null=True)
	reffered_by = models.CharField(max_length=50, blank=True,null=True)
	ref_code = models.CharField(max_length=50, default=rand_str(), blank=True,null=True)
	deposited = models.BooleanField(default=False,  blank=True,null=True)
	bonus = models.IntegerField(default=0, blank=True,null=True)

	
	objects = MyAccountManager()
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return self.is_admin
	
	def  has_module_perms(self, app_label):
		return True





class RefferalProfile(models.Model):
	user = models.OneToOneField(Account, on_delete = models.CASCADE)
	recommended_by = models.ForeignKey(Account,related_name='recom_user', on_delete=models.CASCADE,null=True, blank=True)
	date = models.DateTimeField(auto_now_add=True)
	bonus = models.IntegerField(default=0,blank=True,null=True)


	
	def recom_profies(self):
		qs = RefferalProfile.objects.all()
		my_rec = []
		for profile in qs:
			if profile.recommended_by == self.user:
				my_rec.append(profile)
		return my_rec



	def __str__(self):
		return self.user.username