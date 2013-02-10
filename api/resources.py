# myapp/api.py
from django.contrib.auth.models import User
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization, ReadOnlyAuthorization
from tastypie.validation import FormValidation, CleanedDataFormValidation
from django.shortcuts import get_object_or_404

from tastypie import fields
from django.forms.models import ModelChoiceField
from django.db import IntegrityError

from tastypie.exceptions import BadRequest


from ideas.models import Idea
from ideas.forms import IdeaForm
from forms import UserForm
from api.helpers import AnonymousPostAuthentication, BasicAuthenticationWithCookies, OwnerAuthorization

from ideas.ideas_helpers import uri_to_pk

class ModelFormValidation(FormValidation):
    """
    Override tastypie's standard ``FormValidation`` since this does not care
    about URI to PK conversion for ``ToOneField`` or ``ToManyField``.
    """

    def uri_to_pk(self, uri):
        """
        Returns the integer PK part of a URI.

        Assumes ``/api/v1/resource/123/`` format. If conversion fails, this just
        returns the URI unmodified.

        Also handles lists of URIs
        """

        if uri is None:
            return None

        # convert everything to lists
        multiple = not isinstance(uri, basestring)
        uris = uri if multiple else [uri]

        # handle all passed URIs
        converted = []
        for one_uri in uris:
            try:
                # hopefully /api/v1/<resource_name>/<pk>/
                converted.append(int(one_uri.split('/')[-2]))
            except (IndexError, ValueError):
                raise ValueError(
                    "URI %s could not be converted to PK integer." % one_uri)

        # convert back to original format
        return converted if multiple else converted[0]

    def is_valid(self, bundle, request=None):
        data = bundle.data
        # Ensure we get a bound Form, regardless of the state of the bundle.
        if data is None:
            data = {}
        # copy data, so we don't modify the bundle
        data = data.copy()

        # convert URIs to PK integers for all relation fields
        relation_fields = [name for name, field in
                           self.form_class.base_fields.items()
                           if issubclass(field.__class__, ModelChoiceField)]

        for field in relation_fields:
            if field in data:
                data[field] = self.uri_to_pk(data[field])

        # validate and return messages on error
        form = self.form_class(data)
        if form.is_valid():
            return {}
        return form.errors
    

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
        #excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        
        allowed_methods = ['get', 'post']
        authentication = AnonymousPostAuthentication()
        authorization = Authorization()
        validation = ModelFormValidation(form_class=UserForm)
        
    def obj_create(self, bundle, request=None, **kwargs):
        bundle = super(UserResource, self).obj_create(bundle, request, **kwargs)
        bundle.obj.set_password(bundle.data.get('password'))
        bundle.obj.save() 

        return bundle
    
    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(username=request.user)
    
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
            
#    def alter_list_data_to_serialize(self, request, data):
#        data['public_ideas'] = data['objects']
#        del data['objects']
#        return data
#
#    def alter_deserialized_list_data(self, request, data):
#        data['objects'] = data['public_ideas']
#        del data['locations']
#        return data
