from aem import Query
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import is_safe_url 
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.forms.models import model_to_dict
from isort import file
from joblib import parallel_backend
from matplotlib.style import available

from .models import Room
from .forms import RoomCreationForm 
from bb2.views import c_modify_for_nav, get_user_and_profile

from profiles.models import Profile, Footprint

 




def approve_application(applicants: list, room: Room):
	# add Profile queryset to room.participants if the query doesn't exceed room.max_num
	# returns (message, bool) with the bool indicating if applicants added or not
	if not room.joinable:
		return 'room is not joinable', False
	if not room.max_num:
		room.participants.add(*applicants)
		room.applicants.remove(*applicants)
		return 'applicants added successfully', True
	if room.max_num - len(room.participants.all()) < len(applicants):
		return 'applicants exceed max_num', False
	else:
		room.participants.add(*applicants)
		room.applicants.remove(*applicants)
		room.joinable = False if room.max_num <= len(room.participants.all()) else True
		room.save()
		return 'applicants added successfully', True

def remove_participants(members:list, room: Room):
	# take queryset and remove them from room.participants
	room.participants.remove(*members)
		


def room_info_view(request, slug):
	session_user, profile = get_user_and_profile(request)
	room = Room.objects.get(slug=slug)

	Footprint.objects.create(
		profile = profile,
		kind = 'room_page',
		room_page = room,
	)

	available_action = 'apply'
	if profile in room.participants.all():
		available_action = 'leave'
	elif profile in room.invited.all():
		available_action = 'accept'
	elif profile in room.applicants.all():
		available_action = 'cancel'

	if request.method == 'POST':
		if 'applicants' in request.POST:
			applicants = dict(request.POST).get('applicants')
			applicants = [force_text(urlsafe_base64_decode(x)) for x in applicants]
			applicants = [Profile.objects.get(id=x) for x in applicants]	
			ap_message, ap_success = approve_application(applicants, room)
		if 'participants' in request.POST:
			participants = dict(request.POST).get('participants')
			participants = [force_text(urlsafe_base64_decode(x)) for x in participants]
			participants = [Profile.objects.get(id=x) for x in participants]
			remove_participants(participants, room)

	c = {
		'profile': profile,
		'room':room,
		'owner': room.owner,
		'available_action': available_action,
		'actions': ['accept', 'leave', 'cancel', 'apply'],
		'num_of_members': len(room.participants.all()),
		'applicants' : room.applicants.all(),
		'invited' : room.invited.all(),
		'participants' : room.participants.all(),
		'request': request,
	}
	
	return render(request, 'room_info.html', c)
	

def room_action_view(request, slug, uidb64, action):
	uid = force_text(urlsafe_base64_decode(uidb64)) 
	profile = Profile.objects.get(id=uid)
	room = Room.objects.get(slug=slug)
	if profile != request.user.profile:
		return redirect(reverse('home'))
	if action == 'accept' and profile in room.invited.all():
		room.participants.add(profile)
		room.invited.remove(profile)
	elif action == 'leave':
		room.participants.remove(profile)
	elif action == 'cancel':
		room.applicants.remove(profile)
	elif action=='apply' and profile not in room.participants.all():
		room.applicants.add(profile)
	return room_info_view(request, room.slug)


def room_create_view(request):

	session_user, profile = get_user_and_profile(request)
	if not profile:
		return redirect(reverse('home'))

	c = {
		'form': RoomCreationForm(profile=profile),
	}
	
	if request.method == 'POST':
		form = RoomCreationForm(request.POST, request.FILES, profile=profile) 
		if form.is_valid():
			room = form.save(commit=False)
			room.owner = profile
			room.save()
			room.invited.add(*form.cleaned_data['invited'])
			return redirect(reverse('room_info', kwargs=dict(slug=room.slug)))
	return render(request, 'room_create.html', c)


def room_update_view(request, slug):
	room = Room.objects.get(slug=slug)
	session_user, profile = get_user_and_profile(request)
	if (not profile) or (room.owner != profile):
		return redirect(reverse('home'))

	c = {
		'room': room,
		# for debugging purpose
	}

	if request.method == 'GET':
		c['form'] = RoomCreationForm(initial = model_to_dict(room), profile=profile)
	else:
		form = RoomCreationForm(request.POST, request.FILES, instance=room, profile=profile)
		if form.is_valid():
			form.save()
			c['form'] = RoomCreationForm(request.POST, request.FILES, profile=profile)
			c['update'] = True
		else:
			c['form'] = RoomCreationForm(initial = model_to_dict(room), profile=profile)
	return render(request, 'room_update.html', c)














#---------------using yet?????------ check it when you have time


def leave_accept_apply_view(request, slug, info):
	room = Room.objects.filter(slug = slug)[0]
	session_user, profile = get_user_and_profile(request)
	if not profile:
		return redirect(reverse('room_info', kwargs={'slug': room.slug} ))
	
	if info == 'apply' and room.joinable:
		room.applicants.add(profile)
	elif info == 'accept' and room.joinable:
		room.invited.remove(profile)
		room.participants.add(profile)
	elif info == 'leave':
		room.participants.remove(profile)
	if room.max_num:
		if len(room.participants.all()) >= room.max_num:
			room.joinable = False

	nex = request.GET.get('next', '/')
	if is_safe_url(
		url = nex,
		allowed_hosts = settings.ALLOWED_HOSTS,
		require_https = request.is_secure()
		):
		return redirect(nex)
	return redirect(reverse('home'))



def accept_application_view(request, slug, uidb64):
	uid = force_text(urlsafe_base64_decode(uidb64))
	applicant = Profile.objects.get(pk=uid)
	room = Room.objects.get(slug= slug)
	session_user, profile = get_user_and_profile(request)
	if (not profile) or (room.owner != profile):
		return redirect(reverse('home'))

	if room.owner == profile:
		room.participants.add(applicant)
		room.applicants.remove(applicant)
		if room.max_num:
			if len(room.participants.all()) >= room.max_num:
				room.joinable = False

	nex = request.GET.get('next', '/')
	if is_safe_url(
		url = nex,
		allowed_hosts = settings.ALLOWED_HOSTS,
		require_https = request.is_secure()
		):
		return redirect(nex)
	return redirect(reverse('home'))





