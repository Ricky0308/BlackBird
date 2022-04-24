from django.db import models
from django.forms import ModelForm, DateTimeInput
from django import forms
from sqlalchemy import false
from .models import Room
from profiles.models import Profile



class CustomDateTimeField(forms.SplitDateTimeField):
	def __init__(self, **kwargs):
		self.widget = forms.SplitDateTimeWidget(date_attrs={'type':'date'}, time_attrs={'type':'time'})
		super().__init__(require_all_fields=True, **kwargs)



class RoomCreationForm(ModelForm):
	class Meta:
		model = Room
		fields = [
			'name', 
			'text', 
			'open_time',
			'max_num', 
			'no_apply',
			'reveal_owner',
			'image',
			'invited'
		]

		labels = {
			'max_num' : 'Max number of members',
			'open_time' : 'Time to open the room',
		}

		widgets = {
			'invited': forms.CheckboxSelectMultiple(), 
		} 

	def __init__(self, *arg, profile=None, **kwargs):
		super(RoomCreationForm, self).__init__(*arg, **kwargs)
		self.fields['max_num'].required = False
		self.fields['invited'].required = False
		self.fields['text'].required = True
		self.fields['image'] = forms.ImageField(required=False, widget=forms.FileInput())
		self.fields['open_time'] = CustomDateTimeField()
		if profile:
			self.fields['invited'].queryset = Profile.objects.filter(user__pk__in = profile.follow.all())
		else:
			self.fields['invited'].queryset = Profile.objects.none()




