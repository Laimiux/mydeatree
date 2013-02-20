from django.db import models
from django.contrib.auth.models import User

from friends.fields import ModelListField

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

# Create your models here.    
class FavoriteItem(models.Model):
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')  
    
    
    def save(self, *args, **kwargs):
       ''' On save, update timestamps '''
       import sys
       print >>sys.stderr, 'Saving favorite object'

       
       super(FavoriteItem, self).save(*args, **kwargs)


    


