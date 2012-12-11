from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from djangotoolbox.fields import ListField

from django.forms import ModelForm
from django.forms.widgets import SelectMultiple
from django.forms.fields import MultipleChoiceField

class ModelListField(ListField):
    def formfield(self, **kwargs):
        return FormListField(**kwargs)

class ListFieldWidget(SelectMultiple):
    pass

class FormListField(MultipleChoiceField):
    """
    This is a custom form field that can display a ModelListField as a Multiple Select GUI element.
    """
    widget = ListFieldWidget

    def clean(self, value):
        #TODO: clean your data in whatever way is correct in your case and return cleaned data instead of just the value
        return value


# Create your models here.
class UserProfile(models.Model):  
    """
        A user profile which contains all the extra information 
        user needs.
    """
    # The user to who the profile belongs
    user = models.OneToOneField(User) 
    
    # A list of emails that are user's friends.
    friends = ModelListField(models.ForeignKey(User), null=True, blank=True)
    
    def get_friends(self):
        from itertools import chain
        result_list = []
        
        for friend in self.friends:
            result_list += User.objects.filter(pk__exact=friend)

        return result_list
    
    def __str__(self):  
          return "%s's profile" % self.user  
    
class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['friends'].widget.choices = [(i.pk, i) for i in User.objects.all()]
        if self.instance.pk:
            self.fields['friends'].initial = self.instance.friends
    class Meta:
        model = UserProfile

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=User) 

