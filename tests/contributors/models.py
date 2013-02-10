from django.db import models

from favorites.models import FavoriteObjectList

from generic_models.models import SelfAwareModel


# Create your models here.
class Note(SelfAwareModel):
    title = models.CharField(max_length=30)