
def adjust_for_navbar(request):
    if not request.user.is_anonymous:
        return {'nav_uid': request.user.profile.make_uid(),}
    else:
        return dict()
