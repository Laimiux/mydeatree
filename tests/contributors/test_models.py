"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from tests.contributors.models import Note

from contributors.models import ObjectContributor

from django.contrib.auth.models import User



class ContributorsTest(TestCase):
    
    def test_add_to_contributor(self):
        """
        Tests that adding contributor to item works
        """
        user = User(username="sample", password="password")
        user.save()
        
        note = Note(title="some note")
        note.save()
        
        
        contrib = ObjectContributor(contributor=user, content_object=note)
        
        self.assertEqual(note.pk, contrib.content_object.pk)
        self.assertEqual(user, contrib.contributor)
        
                