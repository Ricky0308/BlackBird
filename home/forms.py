from django import forms 

from profiles.models import Profile
from bb2.lists import (COUNTRY_CHOICES, AGE_CHOICES, 
	PUNCTUALITY_CHOICES, IELTS_SCORE_CHOICES, 
	TOEFL_SCORE_CHOICES, PURPOSE_CHOICES)

class DateInput(forms.DateInput):
	input_type = 'date'


class SearchForm(forms.Form):

	q = forms.CharField(
		required=False, 
		label='free word', 
		max_length=300, 
		widget= forms.TextInput(attrs={'placeholder':'Search...'}))
	kind = forms.MultipleChoiceField(
		required=False, 
		widget=forms.CheckboxSelectMultiple(), 
		choices = (('profile', 'people'),))
	date_from = forms.DateTimeField(
		required=False, 
		widget=DateInput())
	date_to = forms.DateTimeField(
		required=False, 
		widget=DateInput())
	country = forms.MultipleChoiceField(
		required=False, 
		widget=forms.CheckboxSelectMultiple(), 
		choices = [])
	sex = forms.MultipleChoiceField(
		required=False, 
		widget=forms.CheckboxSelectMultiple(), 
		choices = (('female', 'female'), ('male', 'male')))
	age = forms.MultipleChoiceField(
		required=False, 
		widget=forms.CheckboxSelectMultiple(), 
		choices = [])
	punctuality = forms.ChoiceField(
		required=False, 
		initial='no', 
		widget=forms.RadioSelect(), 
		choices = PUNCTUALITY_CHOICES)
	purpose = forms.MultipleChoiceField(
		required=False, 
		widget=forms.CheckboxSelectMultiple(), 
		choices = PURPOSE_CHOICES)

	follow = forms.MultipleChoiceField(
		required=False, 
		widget=forms.CheckboxSelectMultiple(), 
		choices=(('on', 'people you follow'),))
	invited = forms.MultipleChoiceField(
		required=False, 
		widget=forms.CheckboxSelectMultiple(), 
		choices=(('on', 'rooms you are invited'),))
	no_apply = forms.MultipleChoiceField(
		required=False, 
		widget=forms.CheckboxSelectMultiple(), 
		choices=(('on', 'no need to apply'),))
	active = forms.MultipleChoiceField(
		required=False, 
		initial='on', 
		widget=forms.CheckboxSelectMultiple(), 
		choices=(('on', 'active user'),))

	ielts = forms.MultipleChoiceField(
		required=False, 
		widget=forms.CheckboxSelectMultiple(), 
		choices=IELTS_SCORE_CHOICES)
	toefl = forms.MultipleChoiceField(
		required=False, 
		widget=forms.CheckboxSelectMultiple(), 
		choices=TOEFL_SCORE_CHOICES)

	def __init__(self, *args, purpose_initial=None, **kwargs):
		# print(self)
		# print(vaslvnaslkv)
		super().__init__(*args, **kwargs)
		available_country = set(map(lambda x: x.country,Profile.objects.all()))
		AVA_COUNTRY_CHOICES = filter(lambda x: x[0] in available_country, COUNTRY_CHOICES)
		available_age = set(map(lambda x: x.age,Profile.objects.all()))
		AVA_AGE_CHOICES = filter(lambda x: x[0] in available_age, AGE_CHOICES)
		#self.fields['purpose'].initial = purpose_initial
		self.fields['country'].choices = AVA_COUNTRY_CHOICES
		self.fields['age'].choices = AVA_AGE_CHOICES
