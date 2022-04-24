from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.db.models import Q, F, Count, Avg
from django.db import models
from django.utils import timezone

from rooms.models import Room
from profiles.models import Profile, Review, Footprint
from bb2.lists import COUNTRY_LIST, AGE_LIST, PUNCTUALITY_LIST
from bb2.views import c_modify_for_nav, get_user_and_profile
from .forms import SearchForm

from datetime import datetime
import re







def search(request):
	try:
		profile = request.user.profile
		Footprint.objects.create(
			profile = profile,
			kind = 'search',
		)
	except:
		Footprint.objects.create(kind = 'search')
		profile = None
	request_dict = dict(request.GET)
	r_attr = ['age',
	'country',
	'date_from',
	'date_to',
	'follow',
	'invited',
	'no apply',
	'purpose',
	'punctuality',
	'q',
	'sex']
	p_attr = ['age',
	'active',
	'purpose',
	'country',
	'punctuality',
	'q',
	'sex']

	def profile_search(): 
		session_user, profile = get_user_and_profile(request)
		request_dict_p = dict(filter(lambda x: x ,map(lambda x: (x, request_dict[x]) if x in request_dict else None ,p_attr)))

		def age(): 
			q = Profile.objects.none()
			for x in request_dict_p['age']:
				q = q.union(Profile.objects.filter(age__exact = x))
			return q

		def country():
			q = Profile.objects.none()
			for x in request_dict_p['country']:
				q = q.union(Profile.objects.filter(country__exact = x))
			return q

		def sex():
			q = Profile.objects.none()
			for x in request_dict_p['sex']:
				q = q.union(Profile.objects.filter(sex__exact = x))
			return q

		def punctuality():
			if request_dict_p['punctuality'][0] != 'no':
				p_list = Profile.objects.all().annotate(
					average = Avg('reviewee__punctuality')).exclude(average__gt= re.search(r'\d+' ,request_dict_p['punctuality'][0]))
				return Profile.objects.filter(pk__in = p_list)
			return Profile.objects.all()

		def active():
			# return profiles who have more than 10 footprints craeated within 24 hours
			a_day_ago = timezone.now() - timezone.timedelta(days=1)
			num_of_footprints = Count('footprints', 
				filter=Q(footprints__created__range = (a_day_ago, timezone.now()))
			)
			p_list = Profile.objects.annotate(num_of_footprints = num_of_footprints).filter(num_of_footprints__gte=10)
			return Profile.objects.filter(pk__in=p_list)

		def purpose():
			if not request.user.is_anonymous:
				return Profile.objects.filter(purpose__in=request_dict_p['purpose'])
			return Profile.objects.all()
			

		def free_word():
			if words := request_dict_p['q'][0].split():
				name = Profile.objects.all()
				bio = Profile.objects.all()
				for x in words:
					name = name.intersection(
						Profile.objects.filter(last_name__icontains = x)
							.union(Profile.objects.filter(first_name__icontains = x)))
					bio = bio.intersection(
						Profile.objects.filter(bio__icontains = f' {x} '))
				return name.union(bio)
			else:
				return Profile.objects.all()

		qs = []
		funcs = {
			'age' : age,
			'active':active,
			'country': country,
			'punctuality': punctuality,
			'q': free_word,
			'sex': sex,
			'purpose':purpose,
		}

		for x in request_dict_p:
			qs.append(funcs[x]())

		qs = filter(lambda x: x != None, qs)
		if not qs: 
			qs.append(Profile.objects.none())
			if 'profile' in request_dict['kind']:
				qs[0] = Profile.objects.all()
		return Profile.objects.all().intersection(*qs)





	def room_search():
		session_user, profile = get_user_and_profile(request)
		# 
		request_dict_r = dict(filter(
			lambda x: x ,
			map(lambda x: (x, request_dict[x]) if x in request_dict else None ,
				r_attr
		)))
		# 		kwargs ={ f'owner__{x}__contains':y }
		# 		r_query_store['union'].append(Room.objects.filter(Q(**kwargs)))
		
		def invited():
			# if user is AnonymousUser return all Room objects
			try:
				return Room.objects.filter(pk__in = profile.invited.all())
			except:
				return Room.objects.all()

		def follow():
			# if user is AnonymousUser return all Room objects
			try:
				return Room.objects.filter(owner__in = map(lambda x: x.profile ,profile.follow.all()))
			except:
				return Room.objects.all()

		def purpose():
			if profile:
				return Room.objects.filter(owner__purpose__in=request_dict_r['purpose'])
			else:
				return Room.objects.all()

		def punctuality():
			if request_dict_r['punctuality'][0] != 'no':
				p_list = Profile.objects.all().annotate(average = Avg('reviewee__punctuality')).exclude(average__gt= re.search(r'\d+' ,request_dict_r['punctuality'][0]))
				return Room.objects.filter(owner__in = p_list)
			return Room.objects.all()

		def no_apply():
			return Room.objects.filter(no_apply=True)

		def country():
			q = Room.objects.none()
			for x in request_dict_r['country']:
				q = q.union(Room.objects.filter(owner__country__exact = x))
			return q

		def sex():
			q = Room.objects.none()
			for x in request_dict_r['sex']:
				q = q.union(Room.objects.filter(owner__sex__exact = x))
			return q

		def age():
			q = Room.objects.none()
			for x in request_dict_r['age']:
				q = q.union(Room.objects.filter(owner__age__exact = x))
			return q

		def free_word():
			if words := request_dict_r['q'][0].split():
				name = Room.objects.all()
				bio = Room.objects.all()
				for x in words:
					name = name.intersection(
						Room.objects.filter(owner__last_name__icontains = x)
							.union(Room.objects.filter(owner__first_name__icontains = x)))
					bio = bio.intersection(
						Room.objects.filter(owner__bio__icontains = f' {x} '))
				return name.union(bio)

		def date():
			#return Room.objects.all()
			date_from = request_dict_r['date_from'][0]
			date_to = request_dict_r['date_to'][0]
			if date_from:
				date_from = timezone.make_aware(datetime.strptime(date_from, '%Y-%m-%d'))
				if date_from < timezone.localtime():
					date_from = timezone.localtime()
			else :
				date_from = timezone.localtime()

			if date_to:
				date_to = timezone.make_aware(datetime.strptime(date_to, '%Y-%m-%d').replace(hour=23, minute=59))
				if date_to < date_from:
					date_to = ''
			# return [date_from, date_to]
			if date_to:
				return Room.objects.filter(open_time__range=(date_from, date_to))
			else:
				return Room.objects.filter(open_time__gte = date_from)

		qs = []

		funcs = {
			'age' : age,
			'country': country,
			'follow': follow,
			'invited': invited,
			'no apply': no_apply,
			'punctuality': punctuality,
			'q': free_word,
			'sex': sex,
			'purpose':purpose,
		}

		for x in request_dict_r:
			if x not in ['date_from', 'date_to']: 
				qs.append(funcs[x]())
		qs.append(date())

		qs = filter(lambda x: x != None, qs)
		return Room.objects.all().intersection(*qs).order_by('open_time')


	if request.GET.get('kind'):
			search_results = profile_search()
	else:
		search_results= room_search()

	return search_results



















def Home_view(request):
	
	session_user, profile = get_user_and_profile(request)
	initial_data = {}
	if profile: 
		initial_data['purpose'] = session_user.profile.purpose

	c = {
		'COUNTRY_LIST': set(map(lambda x: x.country ,Profile.objects.all())),
		'AGE_LIST': AGE_LIST,
		'PUNCTUALITY_LIST': PUNCTUALITY_LIST,

		'people': request.GET.get('kind'),
		'search_form': SearchForm(initial=initial_data),
		'search_result' : Room.objects.filter(open_time__gte=timezone.now()),
	}


	# search 
	if request.method == 'GET' and request.GET:
		search_form = SearchForm(request.GET)
		reset = bool(request.GET.get('reset'))
		c['search_form'] = [search_form, SearchForm(initial=initial_data)][reset]
		if search_form.is_valid():
			c['search_result'] = search(request)
		else: 
			c['errors']= search_form.errors.as_data()

	c = c_modify_for_nav(request, c)
	return render(request, 'home.html', c)



