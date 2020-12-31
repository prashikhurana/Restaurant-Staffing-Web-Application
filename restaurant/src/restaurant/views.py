from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Prefetch, Sum, Count
from django.db.models import ProtectedError

from .models import Location
from .models import Restaurant
from .models import RestaurantLocation 
from .models import JobPosting
from .models import Application 
from .models import MyUser

from .forms import LocationCreateForm
from .forms import RestaurantCreateForm
from .forms import RestaurantLocationCreateForm
from .forms import JobPostingCreateForm
from .forms import ApplicationCreateForm
from .forms import UserCreationForm

#Location
def location_create_view(request,*args,**kwargs):
	form = LocationCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		form = LocationCreateForm()

	context = {
		'form':form
	}
	return render(request,"location/location_create.html",context);

def location_list_view(request,*args,**kwargs):
	all_locations = Location.objects.all()
	mycontext = {
		'locations':all_locations
	}
	return render(request,"location/location_list.html",mycontext);

def location_delete_view_id(request,id):
	obj = get_object_or_404(Location,id=id)
	if request.method == 'GET':
		try:
			obj.delete()
			return redirect('locationList')
		except ProtectedError:
			error_message = "This Location can't be deleted ," + "Location: " +obj.name 
	context = {
		"locations":Location.objects.all(),
		"error_message":error_message
	}
	return render(request,"location/location_list.html",context)

def location_update_view_id(request,id):
	instance = get_object_or_404(Location,id=id)
	form = LocationCreateForm(request.POST or None, instance=instance)
	if form.is_valid():
		form.save()
		return redirect('locationList')
	return render(request, 'location/location_create.html', {'form': form})  

#restaurant 
def restaurant_list_view(request):
	user = request.user
	if user.usertype == 0 :
		all_restaruant = Restaurant.objects.all()
	else:
		all_restaruant = Restaurant.objects.filter(administrator = request.user)
	mycontext = {
		'all_restaruant':all_restaruant
	}
	return render(request,"restaurant/restaurant_list.html",mycontext);

def restaurant_create_view(request):
	form = RestaurantCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		form = RestaurantCreateForm()
	context = {
		'form':form
	}
	return render(request,"restaurant/restaurant_create.html",context);


#restaurantlocation
def restaurantLocation_list_view(request):
	if request.user.usertype == 0:
		all_restaruant = RestaurantLocation.objects.all()
	else:
		all_restaruant = RestaurantLocation.objects.filter(restaurant__in=Restaurant.objects.filter(administrator= request.user))
	mycontext = {
		'all_restaruant':all_restaruant
	}
	return render(request,"restaurantLocation/restaurant_location_list.html",mycontext);

def restaurantLocation_create_view(request):
	form = RestaurantLocationCreateForm(request.POST or None)
	if form.is_valid():
		att = form.save(commit=False)
		restaurant_queryset = Restaurant.objects.filter(administrator=request.user)
		att.restaurant = restaurant_queryset[0]
		form.save()
		form = RestaurantLocationCreateForm()

	context = {
		'form':form
	}
	return render(request,"restaurantLocation/restaurant_location_create.html",context);

def restaurant_update_view_id(request,id):
	instance = get_object_or_404(RestaurantLocation,id=id)
	form = RestaurantLocationCreateForm(request.POST or None, instance=instance)
	if form.is_valid():
		form.save()
		return redirect('restaurantLocationList')
	return render(request, 'restaurantLocation/restaurant_location_create.html', {'form': form})

def restaurant_delete_view_id(request,id):
	obj = get_object_or_404(RestaurantLocation,id=id)
	error_message = ""
	if request.method == 'GET':
		try:
			obj.delete()
			return redirect('restaurantLocationList')	
		except ProtectedError:
			error_message = "This restaurant location can't be deleted" + "Restaurant: " +obj.restaurant.name + "Location: " +obj.loc.name

	context = {
		"all_restaruant": RestaurantLocation.objects.all(),
		"error_message":error_message
	}
	return render(request,"restaurantLocation/restaurant_location_list.html",context)



#User Views: 
def user_create_view(request,*args,**kwargs):
	form = UserCreationForm(request.POST or None)
	if form.is_valid():
		form.save()
		form = UserCreationForm()

	context = {
		'form':form
	}
	return render(request,"user/user_create.html",context);

def user_list_view(request,*args,**kwargs):
	users_all = MyUser.objects.all()
	mycontext = {
		'all_users':users_all
	}
	return render(request,"user/user_list.html",mycontext);

def user_delete_view_id(request,id):
	obj = get_object_or_404(MyUser,id=id)
	#print(obj, request.method)
	if request.method == 'GET':
		try:
			obj.delete()
			return redirect('userList')
		except ProtectedError:
			error_message = "This user can't be deleted" + "User: " +obj.username
	context = {
		"all_users":MyUser.objects.all(),
		"error_message":error_message
	}
	return render(request,"user/user_list.html",context)

def user_delete_view(request):
	all_users = MyUser.objects.all()
	mycontext = {
		'users':all_users
	}
	return render(request,"user/user_delete.html",mycontext);

def user_update_view(request):
	all_users = MyUser.objects.all()
	mycontext = {
		'users':all_users
	}
	return render(request,"user/user_update.html",mycontext);

def user_update_view_id(request,id):
	instance = get_object_or_404(MyUser,id=id)
	form = UserCreationForm(request.POST or None, instance=instance)
	if form.is_valid():
		form.save()
		return redirect('userList')
	return render(request, 'user/user_create.html', {'form': form}) 


#Job Posting 
def jobPosting_create_view(request,*args,**kwargs):
	form = JobPostingCreateForm(request.POST or None, user=request.user)
	if form.is_valid():
		#form.save()
		att = form.save(commit=False)
		restaurant = Restaurant.objects.filter(administrator = request.user)
		for r in restaurant:
			att.restaurant = r
		form.save()
		form = JobPostingCreateForm(user=request.user)

	context = {
		'form':form
	}
	return render(request,"jobPosting/jobPosting_create.html",context);

def jobPosting_list_view(request,*args,**kwargs):
	user = request.user
	if user.usertype == 0 or user.usertype == 3:
		job_posting = JobPosting.objects.all()
	elif user.usertype == 1:
		job_posting = JobPosting.objects.filter(restaurant_location__in=(RestaurantLocation.objects.filter(restaurant=Restaurant.objects.filter(administrator = user)[0])))
	elif user.usertype == 2:
		if RestaurantLocation.objects.filter(hiring_manager = user) :
			job_posting = JobPosting.objects.filter(restaurant_location=RestaurantLocation.objects.filter(hiring_manager = user)[0])
		else:
			job_posting = None
	mycontext = {
		'all_job_postings':job_posting
	}
	return render(request,"jobPosting/job_posting_list.html",mycontext);

def job_posting_delete_view_id(request,id):
	obj = get_object_or_404(JobPosting,id=id)
	if request.method == 'GET':
		try:
			obj.delete()
			return redirect('jobPostingList')
		except ProtectedError:
			error_message = "This job Posting can't be deleted" + "User: " +obj.name
	context = {
		"all_job_postings":JobPosting.objects.all(),
		"error_message": error_message
	}
	return render(request,"jobPosting/jobPosting_list.html",context)

def jobPosting_update_view_id(request,id):
	instance = get_object_or_404(JobPosting,id=id)
	form = JobPostingCreateForm(request.POST or None, instance=instance, user=request.user)
	if form.is_valid():
		form.save()
		return redirect('jobPostingList')
	return render(request, 'jobPosting/jobPosting_create.html', {'form': form}) 

#Applications 

def application_create_view(request,*args,**kwargs):
	form = ApplicationCreateForm(request.POST or None, user=request.user)
	if form.is_valid():
		att = form.save(commit=False)
		att.user = request.user
		form.save()
		form = ApplicationCreateForm(user=request.user)

	context = {
		'form':form
	}
	return render(request,"application/application_create.html",context);

def application_list_view(request,*args,**kwargs):
	user = request.user
	#print(user.username)
	if user.usertype == 0 or user.usertype == 1:
		all_applications = Application.objects.all()
	elif user.usertype == 2:
		if RestaurantLocation.objects.filter(hiring_manager = user) :
			job_posting = JobPosting.objects.filter(restaurant_location=RestaurantLocation.objects.filter(hiring_manager = user)[0])
			all_applications = Application.objects.filter(job__in=job_posting)
		else:
			all_applications = None
	elif user.usertype == 3:
		all_applications = Application.objects.filter(user = request.user)	
	mycontext = {
		'all_applications':all_applications
	}
	return render(request,"application/applications_list.html",mycontext)

def application_delete_view_id(request,id):
	obj = get_object_or_404(Application,id=id)
	#print("Application Delete",obj, request.method)
	if request.method == 'GET':
		obj.delete()
		return redirect('applicationList')
	context = {
		"object":obj
	}
	return render(request,"application/application_delete.html",context)

def application_update_view_id(request,id):
	instance = get_object_or_404(Application,id=id)
	form = ApplicationCreateForm(request.POST or None, instance=instance, user=request.user)
	if form.is_valid():
		form.save()
		return redirect('applicationList')
	return render(request, 'application/application_create.html', {'form': form}) 


#HOME, LOGIN STUFF
def home_page_view(request,*args,**kwargs):
	mycontext = {
		'user_logged_in':request.user
	}
	return render(request,"home_view.html",mycontext);

def register(request):
	context = {}
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			#print("username",username)
			messages.success(request, f'Account created for {username}!')
			return redirect('home')
		else:
			print(form.errors)
	form = UserCreationForm()
	context = {
				'form':form
			}
	return render(request,"user_regiser.html",context)

@login_required
def profile(request):
	context = {
			'user':request.user
		}
	return render(request,'profile.html',context)

def email1(request,appname,email,id,name,*args,**kwargs):
	s1 = appname
	s2 = email
	instance = get_object_or_404(Application,id=id)
	if name == "Approved":
		instance.approved = 'Approved'
	else:
		instance.approved = 'Rejected'
	instance.save()
	subject = 'This Job Application: '+str(s1)+' has been ' + name + "."
	message = ''
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [s2]
	send_mail( subject, message, email_from, recipient_list )
	return redirect('applicationList')

def all_list_view(request):
	all_applications = Application.objects.all()
	all_users = MyUser.objects.all()
	all_jobPostings = JobPosting.objects.all()
	all_restaruant = Restaurant.objects.all()
	all_restaruant_location = RestaurantLocation.objects.all()
	all_locations = Location.objects.all()

	contex = {
		'all_applications':all_applications,
		'all_users':all_users,
		'all_jobPostings':all_jobPostings,
		'all_restaruant':all_restaruant,
		'all_restaruant_location':all_restaruant_location,
		'all_locations':all_locations,
	}

	return render(request,'all_list.html',contex)