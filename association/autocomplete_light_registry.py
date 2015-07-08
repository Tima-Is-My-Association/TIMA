import autocomplete_light

from association.models import Word
from django.utils.translation import ugettext as _

class WordAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields=['name']
    choice_html_format = '<span class="block os" data-value="%s">%s (%s)</span>'
    attrs={
        'placeholder': _('Filter'),
        'data-autocomplete-minimum-characters': 1,
    }
    widget_attrs={
        'data-widget-maximum-values': 6,
        'class': 'modern-style',
    }

    def choice_html(self, choice):
        return self.choice_html_format % (self.choice_value(choice), self.choice_label(choice), choice.language)
autocomplete_light.register(Word, WordAutocomplete)
