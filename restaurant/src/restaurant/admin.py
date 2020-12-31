from django.contrib import admin
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

# Register your models here.
from .models import Location
admin.site.register(Location)

from .models import Restaurant
admin.site.register(Restaurant)

from .models import RestaurantLocation
admin.site.register(RestaurantLocation)

from .models import JobPosting
admin.site.register(JobPosting)

from .models import Application
admin.site.register(Application)

# from .models import UserLocation
# admin.site.register(UserLocation)

from .models import MyUser
admin.site.register(MyUser)

