from django.shortcuts import render_to_response
from django.template import RequestContext


def main_page(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        current_user = request.user; 
             
        return render_to_response('home.html', { 'user' : current_user}, context_instance=context)
    else:
       
       return render_to_response('home.html', {'registration_form' : ""}, context_instance=context) 
    
 