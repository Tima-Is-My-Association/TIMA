from association.models import Word
from django.db.models import Count
from random import randint

def get_next_word(language, user=None):
    if user and not user.is_anonymous():
        words = Word.objects.filter(languages=language).extra(select={'associationhistory_count': 'SELECT COUNT(*) FROM app_associationhistory JOIN association_association ON association_association.id=app_associationhistory.association_id WHERE association_association.word_id=association_word.id AND user_id=%s'}, select_params=[user.id]).order_by('associationhistory_count', 'count')[:15]
    else:
        words = Word.objects.filter(languages=language).order_by('count')[:15]
    return words[randint(0,14 if words.count() == 15 else words.count())]