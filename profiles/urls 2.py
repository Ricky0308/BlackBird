from django.http import request
from django.urls import path, include, re_path
from . import views 
from django.contrib.auth import views as auth_views
from bb2.views import c_modify_for_nav, get_user_and_profile
from .views import (User_creation_view, 
	user_login_view, profile_update_view,
	profile_taste_view,
	user_logout_view, password_reset_view, 
	account_activation_view, profile_view, 
	follow_view, show_review)


urlpatterns = [

	# profile page
	path('profile/<uidb64>/', profile_view, name='profile'),
	path('profile/update/<uidb64>/', profile_update_view, name='profile_update'),
	path('profile/taste/<uidb64>/', profile_taste_view, name='profile_taste'),

	path('signup/', User_creation_view, name='signup'),
	path('login/', user_login_view, name='login'),
	path('logout/', user_logout_view, name='logout'),

	# follow unfollow 
	path('follow/<uidb64>/', follow_view, name='follow'),

	# review
	path('show_review/<slug>/', show_review, name='show_review'),

	#password 
	path('change-password/', auth_views.PasswordChangeView.as_view(template_name='manager/password_change.html'), 
		name='password_change'),
	path('change-password-done/', 
		auth_views.PasswordChangeDoneView.as_view(
			template_name='manager/password_change_done.html'),
		name='password_change_done'),
	path('reset-password/', password_reset_view, name='password_reset'),
	path('reset-password-done/', auth_views.PasswordResetDoneView.as_view(template_name='manager/password_reset_done.html'),name='password_reset_done'),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='manager/password_reset_confirm.html'),
		name='password_reset_confirm'),
	path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='manager/password_reset_complete.html'),
		name='password_reset_complete'),
	path('activate/<uidb64>/<token>/', account_activation_view, name='account_activation'),
]

