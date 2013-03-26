from django.db import models
    
from django.contrib.auth.models import User

from ideas.models import Idea


class ObjectContributor(models.Model):
    contributor = models.ForeignKey(User)
    idea = models.ForeignKey(Idea)
