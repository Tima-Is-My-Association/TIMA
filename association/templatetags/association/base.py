from association.templatetags.association import register
from association.models import Language, Word

@register.filter
def words(language, exclude=[]):
    return language.words.all() if len(exclude) == 0 else language.words.exclude(id__in=[w.id for w in exclude])

@register.filter
def language(words, language):
    return words.filter(language=language)

@register.filter
def isInNewsletter(word, user):
    return word.newsletters.filter(user=user).exists()
