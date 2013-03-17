"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from django.contrib.auth.models import User

from ideas.models import Idea


def create_user():
    user = User(username="laimis", password="blahblah")
    user.save()
    return user

class IdeaTest(TestCase):
    def test_parent_idea_delete(self):
        """
        Tests that children ideas are deleted when parent idea
        is removed
        """
        user = create_user()
        
        parent = Idea(title="Parent Idea", text="this is the parent idea")
        parent.save()
        
        children = parent.idea_set.create(title="Children Idea", text="this is a children idea")
        
        children_id = children.pk
        parent_id = parent.pk
        
        parent.delete()
        
        self.assertRaises(Idea.DoesNotExist, Idea.objects.get,pk=parent_id)
        self.assertRaises(Idea.DoesNotExist, Idea.objects.get,pk=children_id)
        
    def test_get_children_count(self):
        """
        Tests that get_children_count function returns correct number of children
        """ 
        user = create_user()
        
        idea = Idea(title="Parent Idea", text="this is the parent idea")
        idea.save()
        
        
        self.assertEqual(idea.get_children_count(), 0)
        
        children = idea.idea_set.create(title="Children Idea", text="this is a children idea")
        children.save()
        
        
        self.assertEqual(idea.get_children_count(), 1)
        