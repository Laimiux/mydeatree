"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.utils import unittest
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory

from ideas.models import Idea


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
        
class AdvancedTest(TestCase):
    def test_new_children_idea(self):
        """
        Tests that children idea is properly added
        """
        
class TestURLS(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        
    def test_details(self):
        request = self.factory.get(reverse('new-top-idea'))
        response = my_view(request)
        self.assertEqual(response.status_code, 200)