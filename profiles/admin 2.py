from django.contrib import admin
from .models import Profile, Tag, Review, Footprint, Target


admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Target)
admin.site.register(Review)
admin.site.register(Footprint)
