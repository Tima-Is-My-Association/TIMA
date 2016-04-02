from association.functions.wiktionary import exists
from association.forms import AssociationForm
from association.models import Word
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

class AssociationChainForm(AssociationForm):
    chain_id = forms.IntegerField(required=True, widget=forms.HiddenInput())
