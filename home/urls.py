from django.urls import path, include
from . import views 
from django.contrib.auth import views as auth_views
from .views import Home_view, search

urlpatterns = [
	path('', Home_view, name='home'),
	path('search/', search, name='search'),

]