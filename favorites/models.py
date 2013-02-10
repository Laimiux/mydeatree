from django.db import models
from django.contrib.auth.models import User

from friends.fields import ModelListField

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

# Create your models here.
class Favorite(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

class FavoriteObjectList(models.Model):
    owner = models.ForeignKey(User)

    favorites = ModelListField(models.ForeignKey(Favorite), null=True, blank=True)
    
    class Meta:
        abstract = True
        
        
    def add_to_list(self, obj):
        fav = Favorite(content_object=obj)
        fav.save()
        
        if not self.favorites:
            self.favorites = []

        self.favorites.append(fav.pk)
        self.save()
        
    


