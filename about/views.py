from django.http import Http404
from django.template import TemplateDoesNotExist
from django.views.generic.simple import direct_to_template

# Create your views here.
def about_pages(request, page):
    try:
        return direct_to_template(request, template="%s.html" % page)
    except TemplateDoesNotExist:
        raise Http404()