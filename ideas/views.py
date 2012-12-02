from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from ideas.forms import IdeaForm, CategoryForm
from ideas.models import Idea, Category
from django.template import RequestContext

from django.forms.util import ErrorList

from ideas.utils import convert_to_int

# Create your views here.
def requires_login(view):
    def new_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        return view(request, *args, **kwargs)
    return new_view


def custom_proc(request):
    "A context processor that provides 'app', 'user' and 'ip_address'."
    return {
        'app': 'Mydea',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR']
    }
    
def new_idea(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST,user=request.user)
        if form.is_valid():
            cd = form.cleaned_data
            idea = Idea.objects.create(owner=request.user, title=cd['title'], text=cd['text'], category=cd['category'])
            return HttpResponseRedirect('/')
    else:
        form = IdeaForm(initial={'title': 'I love your site!', 'text' : 'Sample idea!'},user=request.user)
        
        
    return render_to_response('idea_form_top.html', { 'form': form }, context_instance=RequestContext(request))

def new_children_idea(request, id):
     object_id = convert_to_int(id)

     parent_idea = get_object_or_404(Idea, id=object_id, owner=request.user)

     if request.method == 'POST':
        form = IdeaForm(request.POST, owner=request.user)
        if form.is_valid():
            cd = form.cleaned_data
            idea = Idea.objects.create(owner=request.user, title=cd['title'], text=cd['text'], category=cd['category'], parent=parent_idea)
            return HttpResponseRedirect(parent_idea.get_absolute_url())
     else:
        form = IdeaForm(user=request.user,
            initial={'title': 'I love your site!', 'text' : 'Sample idea!'})
        
     return render_to_response('idea_form.html', { 'form': form, 'parent_idea': parent_idea }, context_instance=RequestContext(request))

def show_idea(request, id):
    current_user = request.user
    object_id = convert_to_int(id)      
    parent_idea = get_object_or_404(Idea, id=object_id, owner=request.user)
    children_ideas = parent_idea.idea_set.all()
    return render_to_response('show_children_ideas.html', {'user_name' : current_user, 'parent_idea' : parent_idea, 'idea_list' : children_ideas}, context_instance=RequestContext(request))


def edit_idea(request, id):
    object_id = convert_to_int(id)
    idea = get_object_or_404(Idea, id=object_id, owner=request.user)
    
    if request.method == 'POST':
        form = IdeaForm(request.POST, owner=request.user)
        if form.is_valid():
            cd = form.cleaned_data
            idea.title = cd['title']
            idea.text = cd['text']
            idea.category = cd['category']
            idea.save()
            return HttpResponseRedirect(idea.get_absolute_url())
    else:
        form = IdeaForm(user=request.user, initial={'title':  idea.title, 'text' : idea.text })
        
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
        
def new_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
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
    else:
        form = CategoryForm()
        
    return render_to_response('new_category.html', { 'form' : form}, context_instance=RequestContext(request))
        
def show_categories(request):
    
    categories = Category.objects.filter(owner=request.user)
    
    return render_to_response('show_categories.html', { 'categories' : categories }, context_instance=RequestContext(request) )        


def delete_category(request, id):
    object_id = convert_to_int(id)
    category_to_be_del = get_object_or_404(Category, id=object_id, owner=request.user)
    
    if request.method == "POST":        
        category_to_be_del.delete()     
        return HttpResponseRedirect("/categories/")   
    return render_to_response('category_del_form.html', { 'category' : category_to_be_del }, context_instance=RequestContext(request))
             
def some_page_get(request):
    assert request.method == 'GET'
    #do_something_for_get()
    return render_to_response('show_notes.html')

def some_page_post(request):
    assert request.method == 'POST'
    #do_something_for_post()
    return HttpResponseRedirect('/')

def method_splitter(request, *args, **kwargs):
    get_view = kwargs.pop('GET', None)
    post_view = kwargs.pop('POST', None)
    if request.method == 'GET' and get_view is not None:
        return get_view(request, *args, **kwargs)
    elif request.method == 'POST' and post_view is not None:
        return post_view(request, *args, **kwargs)
    raise Http404



