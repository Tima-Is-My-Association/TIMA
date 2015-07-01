from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

class AssociationForm(forms.Form):
    word = forms.CharField(required=True, widget=forms.HiddenInput())
    association = forms.CharField(required=True,
        widget=forms.TextInput(attrs={'autocomplete':'off',
                                        'class':'form-control',
                                        'placeholder':_('Association')}))

    def clean(self):
        cleaned_data = super(AssociationForm, self).clean()
        word = cleaned_data.get('word')
        association = cleaned_data.get('association')
        if word == association:
            self.add_error('association',
                _('The word and the association may not match.'))
