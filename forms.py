from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs): 
        super(UserForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].error_messages = {'required': "Please enter username"}
        self.fields['username'].max_length = 30
        self.fields['password'].error_messages = {'required': 'Please enter password'}
        self.fields['password'].max_length = 30
        
        self.fields['email'].required = True
              
    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 4:
            raise forms.ValidationError("Username has to be longer than 4 characters")  
        return username
    
    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 5:
            raise forms.ValidationError("Password has to be longer than 5 characters")
        return password 
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
            raise forms.ValidationError("Email address already taken")
        except User.DoesNotExist:
            return email
            
          
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')