from django.conf.urls.defaults import *


from ideas.models import Idea

from ideas.views import *


urlpatterns = patterns('',
    # Authenticated users urls                 
    url(r'^new/$', requires_login(new_top_idea), name="new-top-idea"),

    (r'^idea/(?P<id>\d+)/add/$', requires_login(new_children_idea)),
    (r'^idea/(?P<id>\d+)/del/$', requires_login(delete_idea)),
    (r'^idea/(?P<id>\d+)/edit/$', requires_login(edit_idea)),
    (r'^idea/(?P<id>\d+)/collaboration/$', requires_login(idea_collab)),
    (r'^idea/(?P<id>\d+)/make-public/$', requires_login(make_idea_public)),
    (r'^categories/$', requires_login(show_categories)),
    (r'^categories/(?P<id>\d+)/del/$', requires_login(delete_category)),
    (r'^shared/$', requires_login(show_shared_ideas)),
    (r'^public/new/$', requires_login(new_public_idea)),
    
    #public urls
    (r'^public/$', show_public_ideas),
    (r'^idea/(?P<id>\d+)/$', show_idea),
)
