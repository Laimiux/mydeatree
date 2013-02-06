from django.test import TestCase

class SimpleTest(TestCase):
#    def setUp(self):
#        Player(name='sample').save()
#        
#    def test_setup(self):
#        self.assertEqual(1, len(Player.objects.all()))
#        self.assertEqual('sample', Player.objects.all()[0].content)
#        
    def test_add_favorite(self):
        from favorites.models import Favorite
        from app.models import FavoriteIdeaList
        from ideas.models import Idea
        from django.contrib.auth.models import User
        
        # Create a user
        user = User(username="laimis", password="random").save()
        # Create idea
        idea = Idea(title="some title", text="some text here").save()
        
        fav_list = FavoriteIdeaList(owner=user)
        fav_list.add_to_list(idea)
    