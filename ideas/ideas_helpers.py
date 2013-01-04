from django.utils.functional import wraps
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.template.context import RequestContext

from django.core.serializers.json import DjangoJSONEncoder

from ideas.models import Idea

def get_idea_from_id(view):
    """ 
    Retrieves a specific idea,
    passing it to the view directly
    """
    def wrapper(request, id, *args, **kwargs):
        idea = get_object_or_404(Idea, id=int(id))
        return view(request, idea=idea, *args, **kwargs)
    return wraps(view)(wrapper)
    


def dual_format(template_name):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            data = view(request, *args, **kwargs)
            if request.is_ajax():

                json = simplejson.dumps(data, cls=DjangoJSONEncoder)
                return HttpResponse(json)
            else:
                context = RequestContext(request)
                return render_to_response(template_name, data, context)
        return wraps(view)(wrapper)
    return decorator