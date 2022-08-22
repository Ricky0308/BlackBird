
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.forms.models import model_to_dict

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import PasswordResetForm 
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text

from .models import Profile, Review, Footprint, Tag, Target
from .forms import (ProfileUpdateForm, 
	ProfileCreationForm, TagForm, TargetForm, 
	PurposeForm, EmailAuthenticationForm)
from rooms.models import Room
from bb2.lists import TAG_LIST
from bb2.views import c_modify_for_nav, get_user_and_profile
from bb2.utils import get_or_none

import statistics as st
import uuid




#Profile
def profile_view(request, uidb64):

	uid = force_text(urlsafe_base64_decode(uidb64)) 
	profile = Profile.objects.get(pk=uid)
	profile_user = User.objects.get(profile=profile)
	session_user, session_user_profile = get_user_and_profile(request)
	follows = profile_user.profile.follow.all()

	if session_user_profile:
		Footprint.objects.create(
			profile = session_user_profile,
			kind = 'profile_page',
			profile_page = profile,
		)
	else:
		Footprint.objects.create(
			kind = 'profile_page',
			profile_page = profile,
		)



	c = { 
		'profile_user':profile_user,
		'session_user':session_user,

		'profile':profile,
		'uid' : uidb64,

		'custom_time': timezone.now(),
		'follows' : profile_user.follow.all(),
		'follows_info' : 
		[[x.profile.first_name, x.profile.make_uid()] for x in follows],
		'revealable_info': profile.personal_info(),
		
		'membered_rooms': Room.objects.filter(participants=profile),
		'invited_rooms': Room.objects.filter(invited=profile),
		'owned_rooms': Room.objects.filter(owner=profile, reveal_owner=True),
	}
	if session_user != profile_user and not session_user.is_anonymous:
		c['follow_unfollow'] = ['follow', 'unfollow'][int(profile_user in session_user.profile.follow.all())]

	return render(request, 'profiles/profile.html', c)



#Profile update
def profile_update_view(request, uidb64):
	uid = force_text(urlsafe_base64_decode(uidb64)) 
	profile = Profile.objects.get(pk=uid)
	session_user = request.user

	if session_user.profile != profile:
		return redirect(reverse('home'))

	c = {
		'profile':profile,
		'uid': urlsafe_base64_encode(force_bytes(profile.id)),
	}
	if request.method == 'GET':
		c['form'] = ProfileUpdateForm(initial = model_to_dict(profile))
	else:
		form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
		if form.is_valid():
			form.save()
			c['form'] = ProfileUpdateForm(request.POST, request.FILES)
	return render(request, 'profiles/profile_update.html', c)


def profile_taste_view(request, uidb64):
	uid = force_text(urlsafe_base64_decode(uidb64)) 
	profile = Profile.objects.get(pk=uid)
	session_user = request.user
	if session_user != User.objects.get(profile=profile):
		return redirect(reverse('home'))
	tags_max_num = 15

	c={
		'uid': urlsafe_base64_encode(force_bytes(profile.id)),
		'profile': profile,

		'tags': profile.tags.all(),
		'error_messages': [],
		'success_messages': [],
		'tags_max_num': tags_max_num ,
		'target_errors': [],
	}
	# initialize the forms 
	c['purposeform'] = PurposeForm(initial=model_to_dict(profile))
	profile_tags_dict = {x.lower():profile.tags.filter(kind=x) for x in TAG_LIST}
	c['tagform'] = TagForm(initial=profile_tags_dict)
	initial_target, created = Target.objects.get_or_create(profile=profile)
	c['targetform'] = TargetForm(initial = initial_target.make_dict())

	if request.method == 'POST':
		req_dict = dict(request.POST)

		# deal with purpose
		purposeform = PurposeForm(request.POST, instance=profile)
		if req_dict.get('purpose', [None])[0] != profile.purpose:
			if purposeform.is_valid():
				purposeform.save()
				c['success_messages'].append(f'Purpose updated successfully!')
				c['purposeform'] = purposeform

		# deal with tags
		tagform = TagForm(request.POST)
		c['tagform'] = tagform
		c['targetform'] = TargetForm(request.POST)
		input_tags = set()
		for x in TAG_LIST:
			tagset = {Tag.objects.get(id=id) for id in req_dict.get(x.lower(), [])}
			input_tags=input_tags.union(tagset)
		profile_tags = set(profile.tags.all())
		deleted_tags = profile_tags - input_tags
		added_tags = input_tags - profile_tags
		# update tags associated to request.user.profile 
		# if input_tags doesn't exceed max
		if deleted_tags != added_tags:
			if len(input_tags) <= tags_max_num:
				if tagform.is_valid():
					profile.tags.add(*added_tags)
					profile.tags.remove(*deleted_tags)
					c['success_messages'].append(f'Tags updated successfully!')
			else:
				c['tag_max_error'] = f'You can chose only {tags_max_num} tags ({len(input_tags)} tags are chosen)'
				c['error_messages'].append(f'Tags update failed...')


		# deal with target
		# count numbers of each field's values for targetform
		# replace a particular fields' values that exceed limitations with initial values for the field
		def value_count(field_name, max):
			input_val_num = len(req_dict.get(field_name, []))
			if input_val_num > max:
				c[field_name + '_error'] = f'Up to {max} values for {field_name.capitalize()} ({input_val_num} values chosen).' 
				c['error_messages'].append(f'Target "{field_name}" update failed...')
				req_dict[field_name] = initial_target.make_dict()[field_name]
			else:
				if set(req_dict[field_name]) != set(initial_target.make_dict()[field_name]):
					c['success_messages'].append(f'Target "{field_name}" updated successfully!')
		field_and_max = [
			('sex', 1),
			('country', 5),
			('age', 2),
		]
		for field_name, max in field_and_max:
			value_count(field_name, max)
		targetform = TargetForm(req_dict, instance=profile.target)
		if targetform.is_valid():
			targetform.save() 
		# else:
		# 	c['error']=targetform.errors.as_data()

	c['target_list'] = profile.target.value_list()
	c['allowed_tags_num'] = tags_max_num - len(profile.tags.all())
	return render(request, 'profiles/profile_taste.html', c)




# Review 
def show_review(request, slug):
	review = Review.objects.get(slug=slug)
	c = {
		'review' : review,
		'all_review': Review.objects.all(),
	}
	return render(request, 'profiles/show_review.html', c)


# Follow Unfollow 
def follow_view(request, uidb64):
	# check if the request is valid 
	try: 
		session_user = request.user.profile
		profile_user = Profile.objects.get(pk= force_text(urlsafe_base64_decode(uidb64)))
	except: 
		return redirect(reverse('home'))
	
	# check if the session user already follows profile user
	if session_user != profile_user: 
		
		#already followed
		if profile_user.user not in session_user.follow.all():
			session_user.follow.add(profile_user.user)
		
		# not yet followed
		else:
			session_user.follow.remove(profile_user.user)
		session_user.save()

	return redirect(f'/user/profile/{uidb64}/')

# vajvbak1213131




# User management 
def User_creation_view(request):
	c = {'profile_form': ProfileCreationForm(),
		'user_form': CustomUserCreationForm(),}
	userform_valid, profform_valid = False, False

	if request.method == 'POST':
		c.update({'profile_form': ProfileCreationForm(request.POST),
				'user_form': CustomUserCreationForm(request.POST)})
		prof_form = ProfileCreationForm(request.POST)
		
		if prof_form.is_valid():
			profform_valid = True
		else:
			c.update(dict(prof_form.errors))
			c['p_er'] = prof_form.errors


		request_dict = request.POST.dict()
		user_name = request.POST.get('first_name')
		user_same_name = User.objects.filter(username=user_name)
		while len(user_same_name) >= 1:
			user_name = user_name + str(uuid.uuid4())[:8]
			user_same_name = User.objects.filter(username=user_name)
		request_dict.update({'username': user_name})
		user_form = CustomUserCreationForm(request_dict)
		if user_form.is_valid():
			userform_valid = True
		else:
			c.update(dict(user_form.errors))
			#for development 
			c['u_er'] = user_form.errors


		if profform_valid and userform_valid:
			users_same_email = User.objects.filter(email=request_dict['email'])
			def send_activation_mail(user):
				subject = 'Activate your account'
				email_template_name = 'manager/account_activation_email.txt'
				context = {
					'user' : user,
					'email': user.email,
					'domain':get_current_site(request),
					'uid':urlsafe_base64_encode(force_bytes(user.pk)),
					'token': default_token_generator.make_token(user),
					}
				email = render_to_string(email_template_name, context)
				try:
					send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
				except BadHeaderError:
					return HttpResponse('Invalid header found')

			# check if account with the email address already exists
			if len(users_same_email)==1:
				user = users_same_email[0]
				if not user.is_active:
					send_activation_mail(user)
					return render(request, 'manager/activation_mail_sent.html', c)
				else:
					c.update({'top':['Account already exists']})
					return render(request, 'manager/signup.html', c)
			if len(users_same_email) > 1:
				c.update({'top':['Something going wrong']})
				return render(request, 'manager/signup.html', c)

			# create user and profile and send email
			user = user_form.save(commit=False)
			user.is_active = False
			user.email = request_dict['email']
			user.save()
			profile = prof_form.save(commit=False)
			profile.user = user
			profile.save()				
			send_activation_mail(user)
			return render(request, 'manager/activation_mail_sent.html', c)
	return render(request, 'manager/signup.html', c)


def account_activation_view(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None 
	if user is not None and default_token_generator.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user)
		return redirect(reverse('home'))
	else:
		return HttpResponse('Activation link is invalid!')


def user_login_view(request):
	loginform = EmailAuthenticationForm()
	c = {'loginform' : loginform, }

	if request.method == 'POST':
		loginform = EmailAuthenticationForm(request, data=request.POST)
		if loginform.is_valid():
			email = loginform.cleaned_data.get('email')
			password = loginform.cleaned_data.get('password')
			user = authenticate(request, email=email, password=password)
			if user is not None:
				login(request, user)
				return redirect(reverse('home'))
			else:
				return render(request, 'manager/login.html', c)
	c['debug'] = loginform.errors.values()
	c['errors'] = [x[0] for x in loginform.errors.values()]
	return render(request, 'manager/login.html', c)

def user_logout_view(request):
	logout(request)
	return redirect(reverse('home'))

def password_reset_view(request):
	c = {'form' : PasswordResetForm(),}
	if request.method == 'POST':
		form = PasswordResetForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			c['us'] = associated_users
			if associated_users.exists():
				for user in associated_users:
					subject = 'Password Reset Requested'
					email_template_name = 'manager/password_reset_email.txt'
					context = {
					'user_num' : len(associated_users),
					'name': user.username,
					'email':user.email,
					'domain':get_current_site(request), 
					'uid':urlsafe_base64_encode(force_bytes(user.pk)),
					'user':user,
					'token': default_token_generator.make_token(user),
					'protocol':'http',
					}
					email = render_to_string(email_template_name, context)
					try:
						send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found')
					return redirect(reverse('password_reset_done'))
	return render(request, 'manager/password_reset.html', c)





