"""restaurant_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from restaurant.views import location_list_view 
from restaurant.views import location_create_view 
from restaurant.views import location_delete_view_id
from restaurant.views import location_update_view_id

from restaurant.views import jobPosting_list_view
from restaurant.views import job_posting_delete_view_id
from restaurant.views import jobPosting_create_view
from restaurant.views import jobPosting_update_view_id 

from restaurant.views import user_list_view
from restaurant.views import user_delete_view_id
from restaurant.views import user_delete_view
from restaurant.views import user_create_view 
from restaurant.views import user_update_view
from restaurant.views import user_update_view_id

from restaurant.views import application_list_view
from restaurant.views import application_create_view
from restaurant.views import application_delete_view_id
from restaurant.views import application_update_view_id

from restaurant.views import restaurant_list_view
from restaurant.views import restaurant_create_view
from restaurant.views import restaurant_delete_view_id
from restaurant.views import restaurant_update_view_id

from restaurant.views import restaurantLocation_list_view
from restaurant.views import restaurantLocation_create_view

from restaurant.views import email1
from restaurant.views import home_page_view
from restaurant.views import register
from restaurant.views import profile
from restaurant.views import all_list_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_page_view,name="home"),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name="login"),
    path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'),name="logout"),
    path('register/',register,name="registerAutoUser"),
    path('profile/',profile,name="profile"),
    path('email1<str:appname>/<str:email>/<int:id>/<str:name>',email1,name="email1"),
    path('allList',all_list_view,name='allList'),

    path('location/',location_list_view,name='locationList'),
    path('location_create/',location_create_view,name="locationCreate"),
    path('location_delete_id<int:id>/',location_delete_view_id,name="locationDeleteWithId"),
    path('location_update<int:id>',location_update_view_id,name ="locationUpdateWithId"),
    
    path('jobPosting/',jobPosting_list_view,name='jobPostingList'),
    path('jobPosting_create/',jobPosting_create_view,name="jobPostingCreate"),
    path('jobPosting_delete<int:id>',job_posting_delete_view_id,name="jobPostingDeleteWithId"),
    path('jobPosting_update<int:id>',jobPosting_update_view_id,name="jobPostingUpdateWithId"),
    
    path('users/',user_list_view,name='userList'),
    path('user_create/',user_create_view,name="userCreate"),
    path('user_delete<int:id>/',user_delete_view_id,name="userDeleteWithId"),
    path('user_delete/',user_delete_view,name="userDelete"),
    path('user_update',user_update_view,name="userUpdate"),
    path('user_update<int:id>',user_update_view_id,name="userUpdateWithId"),
    
    path('applications/',application_list_view,name="applicationList"),
    path('application_create/',application_create_view,name="applicationCreate"),
    path('application_delete<int:id>',application_delete_view_id,name="applicationDeleteWithId"),
    path('application_update<int:id>',application_update_view_id,name="applicationUpdateWithId"),
    
    path('restaurant_list/',restaurant_list_view,name="restaurantList"),
    path('restaurant_create/',restaurant_create_view,name="restaurantCreate"),

    path('restaurantLocation_list/',restaurantLocation_list_view,name="restaurantLocationList"),
    path('restaurantLocation_create/',restaurantLocation_create_view,name="restaurantLocationCreate"),
    path('restaurantLocation_delete<int:id>/',restaurant_delete_view_id,name='restaurantLocationDeleteWithId'),
    path('restaurantLocation_update<int:id>',restaurant_update_view_id,name='restaurantLocationUpdateWithId')
    
]
