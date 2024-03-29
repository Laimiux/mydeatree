from django.conf.urls.defaults import *


from ideas.models import Idea

from ideas.views import *
from ideas.ideas_helpers import get_idea_from_id, dual_format


public_idea_dual = dual_format('idea_form.html')
#new_idea_decorator = dual_format('idea_form_top.html')


urlpatterns = patterns('',
    # Authenticated users urls                 
    url(r'^new/$', requires_login(new_idea), 
        { 'template_name' : 'idea_form.html' }, name="new-top-idea"),
    url(r'^idea/(?P<id>\d+)/add/$', requires_login(get_idea_from_id(new_children_idea)), 
        { 'template_name' : 'idea_form.html' }, name="new-children-idea"),
    url(r'^idea/(?P<id>\d+)/del/$', requires_login(get_idea_from_id(delete_idea)), name="delete-idea"),
    url(r'^idea/(?P<id>\d+)/edit/$', requires_login(get_idea_from_id(edit_idea)), name="edit-idea"),
    (r'^idea/(?P<id>\d+)/collaboration/$', requires_login(idea_collab)),
    (r'^idea/(?P<id>\d+)/make-public/$', requires_login(make_idea_public)),
    url(r'^shared/$', requires_login(show_shared_ideas), name="show-shared-ideas"),
    #url(r'^public/new/$', requires_login(new_public_idea), name="new-public-idea"),
    url(r'^public/new/$', public_idea_dual(requires_login(new_public_idea)), name="new-public-idea"),
    
    #public urls
    url(r'^public/$', show_public_ideas, name="show-public-ideas"),
    url(r'^idea/(?P<id>\d+)/$', get_idea_from_id(show_idea), name="show-idea"),
)
