from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q


from .models import Location
from .models import Restaurant
from.models import RestaurantLocation 
from .models import JobPosting
from .models import Application 
from .models import MyUser

class LocationCreateForm(forms.ModelForm):
	class Meta:
		model = Location
		fields = [
			'locationId','name'
		]

class RestaurantCreateForm(forms.ModelForm):
	class Meta:
		model = Restaurant
		fields = [
			'restaurantId','name','administrator'
		]
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['administrator'].queryset = MyUser.objects.filter(usertype=1)

class RestaurantLocationCreateForm(forms.ModelForm):
	class Meta: 
		model = RestaurantLocation
		fields = [
			'loc','hiring_manager'
		]
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		q1 = RestaurantLocation.objects.all()
		hiring_manage_obj = []
		if q1:
			for restaurant_location in q1:
				if restaurant_location.hiring_manager:
					hiring_manage_obj.append(restaurant_location.hiring_manager.username)
			self.fields['hiring_manager'].queryset = MyUser.objects.filter(Q(usertype=2)&~Q(username__in=hiring_manage_obj))
		else:
			self.fields['hiring_manager'].queryset = MyUser.objects.filter(usertype=2)


class JobPostingCreateForm(forms.ModelForm):
	class Meta:
		model = JobPosting
		fields = [
			'jobId','name','restaurant_location',
		]
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		q1 = Restaurant.objects.filter(administrator = self.user)
		super(JobPostingCreateForm,self).__init__(*args, **kwargs)
		self.fields['restaurant_location'].queryset = RestaurantLocation.objects.filter(restaurant__in=q1)
		
class ApplicationCreateForm(forms.ModelForm):
	class Meta:
		model = Application
		fields = [
			'applicationId','job','resume'
		]
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		q1 = Application.objects.filter(user = self.user)
		jobObjId = []
		for app in q1:
			jobObjId.append(app.job.jobId)
		super(ApplicationCreateForm,self).__init__(*args, **kwargs)
		self.fields['job'].queryset = JobPosting.objects.exclude(jobId__in=jobObjId)

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = MyUser
        fields = ("first_name","last_name","username", "email", "password1", "password2","usertype")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user