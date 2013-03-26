"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from django.contrib.auth.models import User

from ideas.models import Idea, Favorite

from django.db import IntegrityError
from django.core.exceptions import ValidationError


def create_user(user='laimis'):
    user = User(username=user, password="blahblah")
    user.save()
    return user

def create_idea(title='Sample Idea', text='Some random idea', public=False,owner=None, parent=None):
    idea = Idea(title=title, text=text, owner=owner, public=public, parent=parent)
    idea.save()
    return idea
    
    

class IdeaTest(TestCase):
    def test_parent_idea_delete(self):
        """
        Tests that children ideas are deleted when parent idea
        is removed
        """
        user = create_user()
        
        parent = create_idea(title="Parent Idea", text="this is the parent idea")
        
        children = parent.idea_set.create(title="Children Idea", text="this is a children idea")
        
        children_id = children.pk
        parent_id = parent.pk
        
        parent.delete()
        
        self.assertRaises(Idea.DoesNotExist, Idea.objects.get,pk=parent_id)
        self.assertRaises(Idea.DoesNotExist, Idea.objects.get,pk=children_id)
        
    def test_cannot_be_own_parent(self):
        idea = create_idea()
        idea.parent = idea
        
        self.assertRaises(ValidationError, idea.save)
        
    def test_no_circle_relationship(self):
        user = create_user()
        parent = create_idea()
        
        children = create_idea(parent=parent)
        
        another_children = create_idea(parent=children)
        
        parent.parent = another_children
        
        self.assertRaises(ValidationError, parent.save)
        
        
        
        
    def test_get_children_count(self):
        """
        Tests that get_children_count function returns correct number of children
        """ 
        user = create_user()
        
        idea = create_idea(title="Parent Idea", text="this is the parent idea")
        
        
        self.assertEqual(idea.get_children_count(), 0)
        
        children = idea.idea_set.create(title="Children Idea", text="this is a children idea")
        children.save()
        
        
        self.assertEqual(idea.get_children_count(), 1)
        
  
class FavoriteTest(TestCase):      
    def test_favorite_uniqueness(self):
        """
        Tests that you cannot create two favorites that have same owner and idea
        """
        user1 = create_user()
        #user2 = create_user(user='kingninja')
        
        idea = create_idea(public=True)
        
        favorite = Favorite(owner=user1, favorite_idea=idea)
        favorite.save()
         
        favorite2 = Favorite(owner=user1, favorite_idea=idea)
        self.assertRaises(IntegrityError, favorite2.save) 
        
    def test_no_self_favorite(self):
        """
        Tests that you cannot favorite your own ideas.
        """
        user = create_user()
        idea = create_idea(owner=user, public=True)
        
        favorite = Favorite(owner=user, favorite_idea=idea)
        
        self.assertRaises(ValidationError, favorite.save)
        
    def test_cannot_favorite_private_ideas(self):
        """
        Tests to make sure that it's not possible to favorite private ideas
        """
        user = create_user()
        idea = create_idea(owner=user)
        
        another_user = create_user(user='kingninja')
        
        favorite = Favorite(owner=another_user, favorite_idea=idea)
        
        self.assertRaises(ValidationError, favorite.save)
        
    def test_favorite_has_to_include_idea(self):
        """
        Tests to make sure that favorite_idea has to be included.
        """
        user = create_user()

        favorite = Favorite(owner=user)
        
        self.assertRaises(ValidationError, favorite.save)
        
    def test_favorite_has_to_include_owner(self):
        """
        Tests to make sure that owner is provided
        """
        idea = create_idea()
        favorite = Favorite(favorite_idea=idea)
        
        self.assertRaises(ValidationError, favorite.save)
        
        
        
        
        

        