from app.models import Profile
from app.templatetags.tima import register

@register.filter
def rank(profile):
    return Profile.objects.filter(points__gt=profile.points).count() + 1
