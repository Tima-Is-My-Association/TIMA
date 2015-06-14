from django import forms

class AssociationForm(forms.Form):
    word = forms.CharField(required=True, widget=forms.HiddenInput())
    association = forms.CharField(required=True, widget=forms.TextInput(attrs={'autocomplete':'off', 'class':'form-control', 'placeholder':'Association'}))