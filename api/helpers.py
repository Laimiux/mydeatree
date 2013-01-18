from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization

from django.contrib.auth.models import User

class AnonymousPostAuthentication(BasicAuthentication):
    """ No auth on post / for user creation """
    def __init__(self, *args, **kwargs):
        super(AnonymousPostAuthentication, self).__init__(*args, **kwargs)
        
    def is_authenticated(self, request, **kwargs):
        """ If POST, don't check auth, otherwise fall back to parent """
        if request.method == "POST":
            return True
        return super(AnonymousPostAuthentication, self).is_authenticated(request, **kwargs)
    
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
    
class OwnerAuthorization(Authorization):
    
    # Optional but useful for advanced limiting, such as per user.
    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            return object_list.filter(owner=request.user)

        return object_list.none()