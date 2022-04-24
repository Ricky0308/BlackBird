from dateutil.tz import tz 
from django.utils import timezone 

class TimezoneMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):

		if hasattr(request.user, 'profile'):
			if request.user.profile.timezone:
				request.session['django_timezone'] = request.user.profile.timezone
				timezone.activate(tz.gettz(request.session['django_timezone']))
		else:
			timezone.deactivate()

		return self.get_response(request)

class FootprintMiddleware:
	# middleware for creating footprints
	pass 