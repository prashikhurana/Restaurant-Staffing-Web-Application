from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.contrib.auth.models import (AbstractBaseUser,PermissionsMixin)
from django.utils import timezone

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, usertype, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            usertype = usertype,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, usertype,password=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
            usertype = usertype,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
	overall_admin = 0
	restaurant_admin = 1
	hiring_manager = 2
	applicant = 3
	ROLE_CHOICES = ((overall_admin,'administrator'),
		(restaurant_admin,'Restaurant_Admin'),
		(hiring_manager,'Hiring Manager'),
		(applicant,'Applicant'))	
	email = models.EmailField(unique=True)
	username = models.CharField(max_length=25, unique=True)
	first_name = models.CharField(max_length=40)
	last_name = models.CharField(max_length=140)
	date_joined = models.DateTimeField(default=timezone.now)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	facility = models.CharField(max_length=140)
	usertype = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
	positiondescription = models.CharField(max_length=140)

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ['username','usertype']

	objects = MyAccountManager()

	def __str__(self):
		return self.username 

	def has_perm(self,perm,obj=None):
		return self.is_admin

	def has_module_perms(self,app_label):
		return True

class Location(models.Model):
	locationId = models.IntegerField()
	name = models.CharField(max_length=150)
	def __str__(self):
		return "%s" % self.name

class Restaurant(models.Model):
	restaurantId = models.IntegerField()
	name = models.CharField(max_length=150)
	administrator = models.OneToOneField(MyUser,on_delete=models.PROTECT)
	def __str__(self):
		return "%s" % self.name
	class Meta:
		unique_together = ("restaurantId","name","administrator")

class RestaurantLocation(models.Model):
	loc = models.ForeignKey(Location, on_delete=models.PROTECT)
	restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
	hiring_manager = models.OneToOneField(MyUser,on_delete=models.PROTECT,null=True, blank=True)
	class Meta:
	 	unique_together = ("restaurant","loc")
	def __str__(self):
		return "%s" % str(self.restaurant.name) +"_"+ str(self.loc.name)

class JobPosting(models.Model):
	jobId = models.IntegerField()
	name = models.CharField(max_length=150)
	restaurant_location = models.ForeignKey(RestaurantLocation, on_delete=models.PROTECT)
	def __str__(self):
		return "%s" % self.name

class Application(models.Model):
	applicationId = models.IntegerField()
	job = models.ForeignKey(JobPosting, on_delete=models.PROTECT)
	user = models.ForeignKey(MyUser, on_delete=models.PROTECT)
	resume = models.CharField(max_length=150)
	approved = models.CharField(max_length=150, default = "Pending")
	class Meta:
		unique_together = ("job","user")