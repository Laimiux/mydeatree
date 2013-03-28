import datetime
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase

from ideas.models import Idea


class FavoriteResourceTest(ResourceTestCase):
    
    def setUp(self):
        super(FavoriteResourceTest, self).setUp()
        
        # Create a user.
        self.username = 'kingninja'
        self.password = 'couldneverguess'
        self.user = User.objects.create_user(self.username, 'someemail@gmail.com', self.password)
        
        self.resource_url = '/api/v1/favorite_ideas/'
        
        
        
        
        self.public_idea = Idea(title='some title', text='some text', public=True, owner=self.user)
        self.public_idea.save()
        
        
        
        # The data we'll send on POST requests. Again, because we'll use it
        # frequently (enough).
        self.post_data = {
            'favorite_idea': '/api/v1/public_ideas/{0}/'.format(self.public_idea.pk)
        }
        
    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password) 
    
    def test_get_list_unauthorized(self):
        self.assertHttpUnauthorized(self.api_client.get(self.resource_url))
        
    def test_get_authorized(self):
        resp = self.api_client.get(self.resource_url, authentication=self.get_credentials())
        self.assertEqual(resp.status_code, 200)
        
    def test_post_favorite_own_idea(self):
        """
        Tests to make sure that you cannot favorite your own favorite idea.
        """
        response = '{"favorite_ideas": {"__all__": ["Cannot favorite your own idea"]}}'
        resp = self.api_client.post(self.resource_url, format='json', data=self.post_data, authentication=self.get_credentials())
        self.assertEqual(resp.content, response)
        self.assertEqual(resp.status_code, 400)

       
       
    def test_post_favorite(self):
        another_user = User.objects.create_user('someuser', 'somil@gmail.com', 'somepassword')
        
        another_idea = Idea(title='some idea', text='some text', public=True, owner=another_user)
        another_idea.save()
        
        post_data = {
                'favorite_idea': '/api/v1/public_ideas/{0}/'.format(another_idea.pk)
                }
        
        resp = self.api_client.post(self.resource_url, format='json', data=post_data, authentication=self.get_credentials()) 
        
        print post_data
        print resp.content
        
        self.assertHttpCreated(resp)
        



