from django.core.mail import send_mail
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from ideas.models import Idea
from django.template import RequestContext
from django.contrib.auth.models import User

import datetime

def main_page(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        current_user = request.user; 
             
        return render_to_response('home.html', { 'user' : current_user}, context_instance=context)
    else:
       
       return render_to_response('home.html', {'registration_form' : ""}, context_instance=context) 
    
 