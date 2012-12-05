from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

from django.views.generic.simple import direct_to_template

import ideas
from ideas import views

from about.views import about_pages
from ideas.views import requires_login

from api import IdeaResource, UserResource
from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(IdeaResource())

admin.autodiscover()

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^admin/', include(admin.site.urls)),
    ('^$', 'views.main_page'),
    (r'^about/$', direct_to_template, {'template' : 'about.html'}),
    (r'^about/(\w+)/$', about_pages),
    (r'^', include('ideas.urls')),
    (r'^', include('contactus.urls')),
    (r'^api/', include(v1_api.urls)),
)



