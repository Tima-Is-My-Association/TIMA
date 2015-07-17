from app.models import AssociationHistory, Profile
from association.models import Word, Association
from django.db.models import Avg
from math import cos

def calculate_points(user, association):
    """Calculates the points for the association.
    Based on the funtion: avg_w / x * y / avg_a * 2
    x: word count
    y: association count
    avg_w: average frequency of a word
    avg_a: average frequency of a association

    Keyword arguments:
    user --- user object
    association --- association object
    """

    x = association.word.count
    y = association.count
    avg_w = Word.objects.filter(language=association.word.language).aggregate(Avg('count'))['count__avg']
    avg_a = Association.objects.filter(word__language=association.word.language).aggregate(Avg('count'))['count__avg']
    points = round(avg_w / x * y / avg_a * 2, 3)
    AssociationHistory.objects.create(user=user if user and not user.is_anonymous() else None, association=association, points=points)
    if user and not user.is_anonymous():
        profile, created = Profile.objects.get_or_create(user=user)
        profile.points += points
        profile.save()

    return points
