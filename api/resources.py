# myapp/api.py
from django.contrib.auth.models import User
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.validation import FormValidation, CleanedDataFormValidation
from django.shortcuts import get_object_or_404

from tastypie import fields
from ideas.models import Idea, Category
from ideas.forms import IdeaForm

from django.forms.models import ModelChoiceField

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
 
 
class BasicAuthenticationWithCookies(BasicAuthentication):
    def __init__(self, *args, **kwargs):
        super(BasicAuthenticationWithCookies, self).__init__(*args, **kwargs)
 
    def is_authenticated(self, request, **kwargs):
        from django.contrib.sessions.models import Session
        if 'sessionid' in request.COOKIES:
            s = Session.objects.get(pk=request.COOKIES['sessionid'])
            if '_auth_user_id' in s.get_decoded():
                u = User.objects.get(id=s.get_decoded()['_auth_user_id'])
                request.user = u
                return True
        return super(BasicAuthenticationWithCookies, self).is_authenticated(request, **kwargs)
    
    
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
        #ordering = ('modified_date',)
        authentication = BasicAuthenticationWithCookies()
        authorization = DjangoAuthorization()
        #validation = FormValidation(form_class=IdeaForm)
        
        
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
        
       
