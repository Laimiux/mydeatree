from django.db import models

from favorites.models import FavoriteObjectList

from ideas.models import Idea

from friends.models import ModelListField
# Create your models here.
class FavoriteIdeaList(FavoriteObjectList):
    pass