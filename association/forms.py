from django import forms
from django.core.exceptions import ValidationError

class AssociationForm(forms.Form):
    word = forms.CharField(required=True, widget=forms.HiddenInput())
    association = forms.CharField(required=True,
        widget=forms.TextInput(attrs={'autocomplete':'off',
                                        'class':'form-control',
                                        'placeholder':'Association'}))

    def clean(self):
        cleaned_data = super(AssociationForm, self).clean()
        word = cleaned_data.get('word')
        association = cleaned_data.get('association')
        if word == association:
            self.add_error('association',
                'Word and association need to be different words.')