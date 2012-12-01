from django.test import TestCase
from djangoappengine.models import Player

class SimpleTest(TestCase):
    def setUp(self):
        Player(name='sample').save()
        
    def test_setup(self):
        self.assertEqual(1, len(Player.objects.all()))
        self.assertEqual('sample', Player.objects.all()[0].content)
        