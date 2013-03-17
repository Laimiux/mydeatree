from django.db import models
from django.contrib.contenttypes import generic

from favorites.models import FavoriteItem

from favorites.signals import remove_favorite_items

class SimpleModel(models.Model):
    text = models.CharField(max_length=30)
    #favorites = generic.GenericRelation(FavoriteItem, null=True)
    def delete(self):
        remove_favorite_items(self)
        super(SimpleModel, self).delete()

