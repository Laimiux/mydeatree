from django.conf.urls.defaults import *

from ideas.models import Idea

from ideas.views import *


urlpatterns = patterns('',
    (r'^new/$', requires_login(new_top_idea)),
    (r'^idea/(?P<id>\d+)/$', requires_login(show_idea)),
    (r'^idea/(?P<id>\d+)/add/$', requires_login(new_children_idea)),
    (r'^idea/(?P<id>\d+)/del/$', requires_login(delete_idea)),
    (r'^idea/(?P<id>\d+)/edit/$', requires_login(edit_idea)),
    (r'^categories/$', requires_login(show_categories)),
    (r'^categories/(?P<id>\d+)/del/$', requires_login(delete_category)),
)
