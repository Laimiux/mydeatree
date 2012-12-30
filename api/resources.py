# myapp/api.py
from django.contrib.auth.models import User
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import ApiKeyAuthentication
from django.shortcuts import get_object_or_404
from tastypie import fields
from ideas.models import Idea, Category

    
class CategoryResource(ModelResource):
    class Meta:
        queryset = Category.objects.all()
        resource_name = 'category'

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(owner=request.user)

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'first_name', 'last_name', 'last_login']
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        
        allowed_methods = ['get']
        # Add it here.
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        
    
    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(username=request.user)
    
    def determine_format(self, request): 
        return "application/json" 
 
  
class IdeaResource(ModelResource):
   # parent = fields.ToOneField('api.resources.IdeaResource', 'parent', full=True, related_name='parent', null=True)
    #children = fields.ToManyField('api.resources.ChildrenIdeaResource', 'idea_set', full=True, related_name='parent')
    
    class Meta:
        queryset = Idea.objects.all()
        resource_name = 'idea'
        list_allowed_methods = ['get', 'post', 'delete', 'head', 'put']
        #excludes = ['id']
        ordering = ('modified_date',)
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        
        
    def obj_create(self, bundle, request=None, **kwargs):
        return super(IdeaResource, self).obj_create(bundle, request, owner=request.user)
        
    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(owner=request.user)
    
    def determine_format(self, request): 
        return "application/json" 
    
class ChildrenIdeaResource(ModelResource):
    #parent = fields.ToOneField(IdeaResource, 'parent')  
    #children = fields.ToManyField('api.resources.ChildrenIdeaResource', 'idea_set', full=True, related_name='parent')
    
    class Meta:
        queryset = Idea.objects.exclude(parent=None)
        resource_name = "children_ideas"
        
       
