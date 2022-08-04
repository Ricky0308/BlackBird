from django.shortcuts import render, redirect, reverse

def get_user_and_profile(request):
    if request.user.is_anonymous:
        return request.user, None
    return request.user, request.user.profile


def c_modify_for_nav(request, context):
    if request.user.is_anonymous:
        return context
    else:
        c = {
            'nav_uid': request.user.profile.make_uid(), 
        }
        context.update(c)
    return context
    
    