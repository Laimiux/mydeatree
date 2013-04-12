from django.shortcuts import render_to_response
from django.template import RequestContext
# Library for creating pagination
from djangoappengine.db.utils import get_cursor, set_cursor

from ideas.models import Idea
from ideas.utils import convert_to_int
from ideas.forms import IdeaForm

def main_page(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        # Get the page number.
        #current_page = convert_to_int(request.GET.get('page') or 1)
        # Number of objects per page
        #results_per_page = 10
        #current_user = request.user; 
        
       # number_of_pages = Idea.objects.filter(owner=request.user, parent=None).count()
        
        #idea_list = Idea.objects.pagination_by_date(results_per_page, current_page)
        #Idea.objects.filter(owner=current_user, parent=None)
        idea_list = Idea.objects.filter(owner=request.user, parent=None).order_by('modified_date').reverse()
                   
                    
#        if number_of_pages % results_per_page != 0:
#            number_of_pages = number_of_pages/results_per_page + 1
#        else:
#            number_of_pages = number_of_pages/results_per_page

        new_idea_form = IdeaForm(owner=request.user)
        
              
        return render_to_response('home.html', { 'user' : request.user, 'idea_form' : new_idea_form,
                                                 'link' : 'api/v1/ideas/','idea_list' : idea_list}, context_instance=context)
    else:
       return render_to_response('home.html', context_instance=context) 
    
def main_backbone(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        new_idea_form = IdeaForm(owner=request.user)
        return render_to_response('home_backbone.html', { 'idea_form' : new_idea_form} , context_instance=context)
    else:
        return render_to_response('home_backbone.html', context_instance=context)
    

 
