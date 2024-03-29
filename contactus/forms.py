from django import forms
from django.forms.widgets import *

# A simple contact form with four fields.
class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    topic = forms.CharField(max_length=30)
    message = forms.CharField(widget=Textarea())