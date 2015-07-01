from app.templatetags.tima import register
from association.models import Association
from datetime import date
from django.utils.numberformat import format
from django.utils.safestring import mark_safe

@register.filter
def floatdot(value, decimal_pos=2):
    if not value:
        return format(0, ",", decimal_pos)
    else:
        return format(round(value, decimal_pos), ",", decimal_pos)
floatdot.is_safe = True

@register.filter
def decrement(value):
    return int(value) - 1

@register.filter
def increment(value):
    return int(value) + 1

@register.filter
def lookup(d, key):
    return d[key] if key in d else None

@register.filter
def previous(value, arg):
    try:
        return value[int(arg) - 1] if int(arg) - 1 != -1 else None
    except:
        return None

@register.filter
def next(value, arg):
    try:
        return value[int(arg) + 1]
    except:
        return None

@register.filter
def startswith(value, start):
    return value.startswith(start)

@register.filter
def endswith(value, start):
    return value.endswith(start)

@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class":css})

@register.filter(name='countassociations')
def countassociations(language):
    return Association.objects.filter(word__languages=language).count()