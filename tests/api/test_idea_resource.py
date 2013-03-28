import datetime
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase


class IdeaResourceTest(ResourceTestCase):
    
    def setUp(self):
        super(IdeaResourceTest, self).setUp()
        
        # Create a user.
        self.username = 'kingninja'
        self.password = 'couldneverguess'
        self.user = User.objects.create_user(self.username, 'someemail@gmail.com', self.password)
        
        self.resource_url = '/api/v1/idea/'
        
    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password) 
    
    def test_get_list_unauthorized(self):
        self.assertHttpUnauthorized(self.api_client.get(self.resource_url))
        
    def test_get_authorized(self):
        resp = self.api_client.get(self.resource_url, authentication=self.get_credentials())
        self.assertEqual(resp.status_code, 200)
        
         

        