from django import forms
from friends.models import UserProfile

from django.contrib.auth.models import User

class FriendForm(forms.Form):
    email = forms.EmailField(label=("E-mail"), max_length=75)

    def clean_email(self):
#        """ Ensure that the supplied email address is unique. """
#        if self.cleaned_data['email']:
#            raise forms.ValidationError((u'This email address is already in use. Please supply a different email address.'))
        return self.cleaned_data['email']
    
