from django.urls import path, include, re_path
from . import views 
from .views import (room_info_view, room_create_view, 
	room_update_view,leave_accept_apply_view, 
	accept_application_view, room_action_view
)

urlpatterns = [
	path('room_info/<str:slug>/', room_info_view, name='room_info'),
	path('room_create/', room_create_view, name='room_create'),
	path('room_update/<str:slug>/', room_update_view, name='room_update'),
	path('room_action/<str:slug>/<str:uidb64>/<str:action>/', room_action_view, name='room_action'),
	path('leave_accept_apply/<str:slug>/<str:info>/', leave_accept_apply_view, name='leave_accept_apply'),
	path('accept_application/<str:slug>/<str:uidb64>/', accept_application_view, name='accept_application'),
]




