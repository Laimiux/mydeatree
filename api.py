# myapp/api.py
from django.contrib.auth.models import User
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import ApiKeyAuthentication
from tastypie import fields
from ideas.models import Idea


class IdeaAuthorization(Authorization):
    def apply_limits(self, request, object_list=None):
        if request and request.method in ('GET', 'DELETE'):  # 1.
            return object_list.filter(author=request.user)
 
        if isinstance(object_list, Bundle):  # 2.
            bundle = object_list # for clarity, lets call it a bundle            
            bundle.data['author'] = {'pk': request.user.pk}  # 3.
            return bundle
 
        return []  # 4.


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'first_name', 'last_name', 'last_login']
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        #allowed_methods = ['get']
        # Add it here.
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        
class IdeaResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    
    class Meta:
        queryset = Idea.objects.all()
        resource_name = 'idea'
        authentication = ApiKeyAuthentication()
        filtering = {
            'user': ALL_WITH_RELATIONS,
        }
        

