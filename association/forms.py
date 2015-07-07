from association.models import Word
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

class AssociationForm(forms.Form):
    word = forms.CharField(required=True, widget=forms.HiddenInput())
    language = forms.CharField(required=True, widget=forms.HiddenInput())
    association = forms.CharField(required=True,
        widget=forms.TextInput(attrs={'autocomplete':'off',
                                        'class':'form-control',
                                        'placeholder':_('Association')}))
    association1 = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super(AssociationForm, self).clean()
        word = cleaned_data.get('word')
        association = cleaned_data.get('association')
        if word == association:
            self.add_error('association',
                _('The word and the association may not match.'))

        a = cleaned_data['association'] if 'association' in cleaned_data else ''
        if not Word.objects.filter(name=a).filter(language__code=cleaned_data.get('language')).exists() and (not cleaned_data.get('association1') or cleaned_data.get('association1') != a):
                self.add_error('association',
                    _('We have not recognized your input as word.' +
                            ' Are you sure you have no spelling mistakes,' + 
                            ' in order to confirm your input press "Save".'))
        cleaned_data['association1'] = a
