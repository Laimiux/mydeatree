from django.conf.urls.defaults import *


from ideas.models import Idea

from ideas.views import *
from ideas.ideas_helpers import get_idea_from_id


urlpatterns = patterns('',
    # Authenticated users urls                 
    url(r'^new/$', requires_login(new_top_idea), name="new-top-idea"),

    url(r'^idea/(?P<id>\d+)/add/$', requires_login(get_idea_from_id(new_children_idea)), name="new-children-idea"),
    url(r'^idea/(?P<id>\d+)/del/$', requires_login(delete_idea), name="delete-idea"),
    url(r'^idea/(?P<id>\d+)/edit/$', requires_login(edit_idea), name="edit-idea"),
    (r'^idea/(?P<id>\d+)/collaboration/$', requires_login(idea_collab)),
    (r'^idea/(?P<id>\d+)/make-public/$', requires_login(make_idea_public)),
    (r'^categories/$', requires_login(show_categories)),
    (r'^categories/(?P<id>\d+)/del/$', requires_login(delete_category)),
    url(r'^shared/$', requires_login(show_shared_ideas), name="show-shared-ideas"),
    (r'^public/new/$', requires_login(new_public_idea)),
    
    #public urls
    url(r'^public/$', show_public_ideas, name="show-public-ideas"),
    (r'^idea/(?P<id>\d+)/$', get_idea_from_id(show_idea)),
)
