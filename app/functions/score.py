from app.models import AssociationHistory, Profile
from math import cos

def calculate_points(user, association):
    """Calculates the points for the association.
    Based on the funtion: max(b * cos(x/700) * cos(y/400), 1)
    b: base points
    x: word count
    y: association count

    Keyword arguments:
    user --- user object
    association --- association object
    """
    BASE_POINTS = 10

    x = association.word.count
    y = association.count
    points = round(max(BASE_POINTS * cos(x / 700) * cos(y / 400), 1), 3) if x <= 1150 and y <= 650 else 1
    AssociationHistory.objects.create(user=user, association=association, points=points)
    profile, created = Profile.objects.get_or_create(user=user)
    profile.points += points
    profile.save()

    return points