"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from favorites.models import FavoriteItem
from tests.favorites.models import SimpleModel

from django.contrib.auth.models import User

from ideas.models import Idea

def createUser():
    user = User(username="laimis", password="blahblah")
    user.save()
    return user

def createSimpleModel():
    mod = SimpleModel(text="some random text here")
    mod.save()
    return mod

class FavoriteTest(TestCase):
    def test_removal_gfk(self):
        """
        Tests that FavoriteItem is removed when Generic Foreign Key is deleted
        """
        user = createUser()
        mod = createSimpleModel()
        
        fav = FavoriteItem(user=user, content_object=mod)
        fav.save()
        
        model_id = mod.pk
        favorite_item_id = fav.pk
        
        
        #self.assertEqual(fav.content_object, mod)
        
        mod.delete()
        
        self.assertEqual(fav.content_object, None)
        self.assertRaises(FavoriteItem.DoesNotExist, FavoriteItem.objects.get,pk=favorite_item_id)
        
    
    def test_add_to_list(self):
        """
        Tests that adding to favorite list object works
        """
        user = createUser()
        
        idea = Idea(title="some title", text="some text i write")
        idea.save()
        
        fav = FavoriteItem(user=user, content_object=idea)

        self.assertEqual(idea.pk, fav.content_object.pk)
        