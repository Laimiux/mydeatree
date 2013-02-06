"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


from tests.favorites.models import FavoriteSolidList

from favorites.models import Favorite

from django.contrib.auth.models import User

from ideas.models import Idea

class FavoriteTest(TestCase):
    def test_add_to_list(self):
        """
        Tests that adding to favorite list object works
        """
        user = User(username="laimis", password="blahblah")
        user.save()
        
        idea = Idea(title="some title", text="some text i write")
        idea.save()
        
        fav_list = FavoriteSolidList(owner=user)
       # fav_list.save()
        
        fav_list.add_to_list(idea)
        
        fav = Favorite.objects.get(pk=fav_list.favorites[0])
        
        self.assertEqual(idea.pk, fav.content_object.pk)
        