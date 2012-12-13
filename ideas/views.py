from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from ideas.forms import IdeaForm, CategoryForm
from ideas.models import Idea, Category
from django.template import RequestContext

from django.forms.util import ErrorList

from ideas.utils import convert_to_int

# Requires login function
def requires_login(view):
    def new_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        return view(request, *args, **kwargs)
    return new_view
    
def new_top_idea(request):
    form = IdeaForm(request.POST or None, initial={'title': 'I love your site!', 'text' : 'Sample idea!'}, user=request.user)
    if form.is_valid():
        model = form.save()
        model.owner = request.user
        model.save()
        return HttpResponseRedirect('/')
    return render_to_response('idea_form_top.html', { 'form': form }, context_instance=RequestContext(request))

def new_children_idea(request, id):
     object_id = convert_to_int(id)
     parent_idea = get_object_or_404(Idea, id=object_id, owner=request.user)
     form = IdeaForm(request.POST or None, initial={'title': 'I love your site!', 'text' : 'Sample idea!'}, user=request.user)
     if form.is_valid():
        model = form.save()
        model.owner = request.user
        model.parent = parent_idea
        model.save()
        return HttpResponseRedirect(parent_idea.get_absolute_url())
     return render_to_response('idea_form.html', { 'form': form, 'parent_idea': parent_idea }, context_instance=RequestContext(request))

def show_idea(request, id):
    # Get the page number.
    current_page = convert_to_int(request.GET.get('page') or 1)
    # Number of objects per page
    results_per_page = 10
    current_user = request.user; 
    
    object_id = convert_to_int(id)      
    parent_idea = get_object_or_404(Idea, id=object_id, owner=request.user)
        
    number_of_pages = parent_idea.idea_set.all().count()
    
    if number_of_pages % results_per_page != 0:
        number_of_pages = number_of_pages/results_per_page + 1
    else:
        number_of_pages = number_of_pages/results_per_page
    
    

    children_ideas = parent_idea.idea_set.all().order_by('modified_date').reverse()[results_per_page*(current_page-1):current_page*results_per_page]
    
    return render_to_response('show_children_ideas.html', { 'user_name' : current_user, 'idea_list' : children_ideas, 
                                  'parent_idea' : parent_idea, 'number_of_pages' : number_of_pages, 
                                                'current_page' : current_page}, context_instance=RequestContext(request))

def idea_collab(request, id):
    current_user = request.user; 
    
    object_id = convert_to_int(id)      
    parent_idea = get_object_or_404(Idea, id=object_id, owner=request.user)
        
    return render_to_response('idea_collaboration.html', { 'user_name' : current_user,
                                  'parent_idea' : parent_idea,}, context_instance=RequestContext(request))



def edit_idea(request, id):
    object_id = convert_to_int(id)
    idea = get_object_or_404(Idea, id=object_id, owner=request.user)
    form = IdeaForm(request.POST or None, user=request.user, instance=idea)
    if form.is_valid():
        idea = form.save()
        return HttpResponseRedirect(idea.get_absolute_url())
        
    return render_to_response('idea_edit_form.html', { 'form': form }, context_instance=RequestContext(request))

    

def delete_idea(request, id):
    object_id = convert_to_int(id)
    idea_to_be_deleted = get_object_or_404(Idea, id=object_id, owner=request.user)
    
    if request.method == "POST":
        if idea_to_be_deleted.parent is not None:
            returned = idea_to_be_deleted.parent.get_absolute_url()
        else:
            returned = "/"
            
        idea_to_be_deleted.delete()
        
        return HttpResponseRedirect(returned)
    
    return render_to_response('delete_form.html', { 'idea' : idea_to_be_deleted }, context_instance=RequestContext(request))
            
def show_categories(request):
    
    categories = Category.objects.filter(owner=request.user)
    
    # Sticks in a post or renders empty form
    form = CategoryForm(request.POST or None)

    if form.is_valid():
        cd = form.cleaned_data
        try:
            #Add better checking for same categories
            duplicates = Category.objects.get(name=cd['name'], owner=request.user)

            errors = form._errors.setdefault("name", ErrorList())
            errors.append(u"There already exists a category with such name")
        except Category.DoesNotExist:
            category = Category.objects.create(owner=request.user, name=cd['name'])
            return HttpResponseRedirect('/categories/')

    return render_to_response('show_categories.html', { 'categories' : categories, 'form': form, 'layout': 'inline', }, context_instance=RequestContext(request))        


def delete_category(request, id):
    object_id = convert_to_int(id)
    category_to_be_del = get_object_or_404(Category, id=object_id, owner=request.user)
    
    if request.method == "POST":        
        category_to_be_del.delete()     
        return HttpResponseRedirect("/categories/")   
    return render_to_response('category_del_form.html', { 'category' : category_to_be_del }, context_instance=RequestContext(request))
             



