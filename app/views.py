from django.shortcuts import render_to_response
from django.template import RequestContext

def angular_view(request):
    context = RequestContext(request)
    return render_to_response('index.html', context_instance=context)