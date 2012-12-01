from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from contactus.forms import ContactForm
from django.core.mail import send_mail, BadHeaderError

from google.appengine.api.mail import EmailMessage

# Create your views here.
def contact_us(request):   
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            msg = EmailMessage()
            msg.sender = 'limeblaststudios@gmail.com'
            msg.to = 'laimiux@gmail.com'
            msg.subject = cd['topic']
            msg.body = "From " + cd['name'] + " at " + cd['email'] + " Message: " + cd['message']
            #msg = "From " + cd['name'] + " at " + cd['email'] + " Message: " + cd['message']
            #send_mail(cd['topic'], msg, cd['email'], ['laimiux@gmail.com'])
            msg.send()
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm()       
    return render_to_response('contact_form.html', { 'form' : form }, context_instance=RequestContext(request))

def thank_you(request):
    return render_to_response('thank_you.html', context_instance=RequestContext(request))