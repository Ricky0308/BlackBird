from profiles.forms import Reviewform
from profiles.models import Review


def adjust_for_navbar(request):
    if not request.user.is_anonymous:
        return {'nav_uid': request.user.profile.make_uid(),}
    else:
        return dict()

def show_reviewform(request):
    if not request.user.is_anonymous:
        profile = request.user.profile
        if qs := Review.objects.filter(reviewer = profile):
            review = qs[0]
            reviewform = Reviewform(instance=review)
            return {'reviewform': reviewform,}
    return dict()