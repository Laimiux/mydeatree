# myapp/api.py
from django.contrib.auth.models import User
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization, ReadOnlyAuthorization
from tastypie.validation import CleanedDataFormValidation
from django.shortcuts import get_object_or_404

from tastypie import fields

from django.db import IntegrityError

from tastypie.exceptions import BadRequest


from ideas.models import Idea, Favorite
from ideas.forms import IdeaForm, FavoriteForm
from forms import UserForm
from api.helpers import AnonymousPostAuthentication, BasicAuthenticationWithCookies, OwnerAuthorization

from ideas.ideas_helpers import uri_to_pk

from django.core.urlresolvers import reverse
from django.conf import settings

from tastypie.contrib.contenttypes.fields import GenericForeignKeyField

from api.validation import ModelFormValidation

class UsernameResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get']
        authentication = BasicAuthentication()
        authorization = ReadOnlyAuthorization()
        fields = ['username']
        include_resource_uri = False
    
    def determine_format(self, request): 
        return "application/json"     
 

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'email', 'public', 'first_name', 'last_name', 'last_login', 'password']

        allowed_methods = ['get']
        authentication = BasicAuthentication()
        authorization = Authorization()
        validation = ModelFormValidation(form_class=UserForm)
        
#    def obj_create(self, bundle, request=None, **kwargs):
#        bundle = super(UserResource, self).obj_create(bundle, request, **kwargs)
#        bundle.obj.set_password(bundle.data.get('password'))
#        bundle.obj.save() 
#
#        return bundle
    
    def apply_authorization_limits(self, request, object_list):
        if request and request.user:
            return object_list.filter(username=request.user)
        else:
            return []
    
    def determine_format(self, request): 
        return "application/json" 
  
class IdeaResource(ModelResource):
    parent = fields.ToOneField('api.resources.IdeaResource', 'parent', related_name='children', null=True, full=False)
    
    class Meta:
        always_return_data = True
        queryset = Idea.objects.all()
        resource_name = 'idea'
        list_allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = BasicAuthenticationWithCookies()
        authorization = OwnerAuthorization()
        limit = 100
        
        ordering = ['modified_date']
        
        filtering = {
            "parent" : ALL,
            "modified_date" : ['gt', 'lt']
        }
        validation = ModelFormValidation(form_class=IdeaForm)
                
    def obj_create(self, bundle, request=None, **kwargs):
        if request and hasattr(request, 'user'):
            return super(IdeaResource, self).obj_create(bundle, request, owner=request.user, **kwargs)
        else:
            return super(IdeaResource, self).obj_create(bundle, request, **kwargs)
        
        
    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(owner=request.user)

    
    def determine_format(self, request): 
        return "application/json" 
    
class PublicIdeaResource(ModelResource):  
    parent = fields.ToOneField('api.resources.PublicIdeaResource', 'parent', related_name='children', null=True, full=False)
    owner = fields.ToOneField('api.resources.UsernameResource', 'owner', related_name='user', null=True, full=True)

    class Meta:
        queryset = Idea.objects.filter(public=True)
        list_allowed_methods = ['get']
        resource_name = "public_ideas"
        authentication = Authentication()
        authorization = ReadOnlyAuthorization()
        
    def determine_format(self, request): 
        return "application/json" 
    
    def dehydrate(self, bundle):
        #include number of direct children
        public_children_count = Idea.objects.get(pk=bundle.data['id']).idea_set.filter(public=True).count()
        bundle.data['children_count'] = public_children_count 
        #include a link for public ideas
        # bundle.data['link'] = settings.WEB_BASE + reverse('show-idea', args=(bundle.data['id'],))
        return bundle
    
    # Makes sure if parent isn't public not to show its uri.
    def dehydrate_parent(self, bundle):
        parent_uri = bundle.data['parent']
        if parent_uri is None:
            return parent_uri
        else:
            parent_id = uri_to_pk(parent_uri)
            try:
                self.Meta.queryset.get(pk=parent_id)
                return parent_uri
            except Idea.DoesNotExist:
                return None
            
class FavoriteIdeaResource(ModelResource):
   # idea = fields.ToOneField('api.resources.PublicIdeaResource', 'favorite_idea', related_name='favorites', null=True, full=False)
    owner = fields.ToOneField('api.resources.UserResource', 'owner')
    favorite_idea = fields.ToOneField('api.resources.PublicIdeaResource', 'favorite_idea', null=True, full=False)
    
    class Meta:
        list_allowed_methods = ['get', 'post', 'delete']
        resource_name = 'favorite_ideas'
        queryset = Favorite.objects.all()
        authentication = BasicAuthenticationWithCookies()
        authorization = OwnerAuthorization()

        validation = ModelFormValidation(form_class=FavoriteForm)
            
    def determine_format(self, request): 
        return "application/json" 
    
    def obj_create(self, bundle, request=None, **kwargs):
        return super(FavoriteIdeaResource, self).obj_create(bundle, request, **kwargs)
#        if request and hasattr(request, 'user'):
#            return super(FavoriteIdeaResource, self).obj_create(bundle, request, owner=request.user, **kwargs)
#        else:
#            return super(FavoriteIdeaResource, self).obj_create(bundle, request, **kwargs)


    def full_hydrate(self, bundle, request=None):
        # Put owner pk from request
        bundle.data['owner'] = bundle.request.user.pk
        return bundle  
    
    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(owner=request.user)
    
 
class ContributorResource(ModelResource):
    idea = fields.ToOneField('api.resources.IdeaResource', 'idea', related_name='contributor', null=True, full=False) 
    user = fields.ToOneField('api.resources.UsernameResource', 'owner', related_name='user', null=True, full=True)  




#    def alter_list_data_to_serialize(self, request, data):
#        data['public_ideas'] = data['objects']
#        del data['objects']
#        return data
#
#    def alter_deserialized_list_data(self, request, data):
#        data['objects'] = data['public_ideas']
#        del data['locations']
#        return data
