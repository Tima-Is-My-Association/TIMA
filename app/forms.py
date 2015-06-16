from django import forms
from django.contrib.auth.forms import UserChangeForm as AuthUserChangeForm, UserCreationForm as AuthUserCreationForm
from django.contrib.auth.models import User

class UserChangeForm(AuthUserChangeForm):
    cultural_background = forms.CharField(required=False, widget=forms.TextInput(attrs={'autocomplete':'off', 'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'autocomplete':'off', 'class':'form-control'})
        self.fields['email'].widget = forms.TextInput(attrs={'autocomplete':'off', 'class':'form-control'})
        self.fields['first_name'].widget = forms.TextInput(attrs={'autocomplete':'off', 'class':'form-control'})
        self.fields['last_name'].widget = forms.TextInput(attrs={'autocomplete':'off', 'class':'form-control'})

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

class UserCreationForm(AuthUserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'autocomplete':'off', 'class':'form-control'})
        self.fields['password1'].widget = forms.TextInput(attrs={'autocomplete':'off', 'class':'form-control'})
        self.fields['password2'].widget = forms.TextInput(attrs={'autocomplete':'off', 'class':'form-control'})