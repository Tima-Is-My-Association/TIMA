from association.models import Word
from django.db.models import Count

def get_next_word(language, user=None):
    if user:
        return Word.objects.filter(languages=language).filter(word__associationhistory__user=user).annotate(associationhistory_count=Count('word__associationhistory')).order_by('associationhistory_count', 'count', '?').first()
    else:
        return Word.objects.filter(languages=language).order_by('count', '?').first()