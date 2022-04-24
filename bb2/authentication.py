from django.contrib.auth.backends import ModelBackend, UserModel
from django.contrib.auth.models import User


class EmailBackend(ModelBackend):
	def authenticate(self, request, email=None, password=None, **kwargs):
		if email is None or password is None:
			return None
		try:
			user = User.objects.get(email=email)
		except UserModel.DoesNotExist:
			UserModel().set_password(password)
		else:
			if user.check_password(password) and self.user_can_authenticate(user):
				return user



##### for debugging 
from django.views.decorators.debug import sensitive_variables
from django.contrib.auth import _get_backends, _clean_credentials
import inspect
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
@sensitive_variables("credentials")
def authenticate(request=None, **credentials):
	"""
	If the given credentials are valid, return a User object.
	"""
	x = _get_backends(return_tuples=True)
	for backend, backend_path in _get_backends(return_tuples=True):
		backend_signature = inspect.signature(backend.authenticate)
		try:
			backend_signature.bind(request, **credentials)
		except TypeError:
			# This backend doesn't accept these credentials as arguments. Try
			# the next one.
			continue

		try:
			user = backend.authenticate(request, **credentials)
			if backend_path == 'bb2.authentication.DebugBackend':
				pass
			#### this is credentials {'email': 'green0308@softbank.ne.jp', 'password': 'ryoryo0308'}
		except PermissionDenied:
			# This backend says to stop in our tracks - this user should not be
			# allowed in at all.
			break
		if user is None:
			if backend_path not in ('bb2.authentication.DebugBackend', 'bb2.authentication.EmailBackend'):
				pass
			continue
		# Annotate the user object with the path of the backend.
		user.backend = backend_path
		return user

	# The credentials supplied are invalid to all backends, fire signal
	user_login_failed.send(
		sender=__name__, credentials=_clean_credentials(credentials), request=request
	)

#### for debugging 
from django.contrib.auth.backends import ModelBackend
class DebugBackend(ModelBackend):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def authenticate(self, request, username=None, password=None, **kwargs):
		if username is None:
			username = kwargs.get(UserModel.USERNAME_FIELD)
		if username is None or password is None:
			return
		try:
			user = UserModel._default_manager.get_by_natural_key(username)
		except UserModel.DoesNotExist:
			# Run the default password hasher once to reduce the timing
			# difference between an existing and a nonexistent user (#20760).
			UserModel().set_password(password)
		else:
			if user.check_password(password) and self.user_can_authenticate(user):
				return user
		