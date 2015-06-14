from association.models import Word
def get_next_word(language):
    return Word.objects.filter(languages=language).order_by('count', '?').first()