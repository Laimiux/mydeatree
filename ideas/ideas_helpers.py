from django.utils.functional import wraps
from django.shortcuts import get_object_or_404, render_to_response
from django.template.loader import get_template
from django.template.context import RequestContext
from django.http import HttpResponseRedirect

from django.core.serializers.json import DjangoJSONEncoder

from ideas.models import Idea

from django.utils import simplejson


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
                if 'redirect' in data:
                    return HttpResponseRedirect(data['redirect'])
                else:
                    return render_to_response(template_name, data, context)
        return wraps(view)(wrapper)
    return decorator

def uri_to_pk(uri):
        """
        Returns the integer PK part of a URI.

        Assumes ``/api/v1/resource/123/`` format. If conversion fails, this just
        returns the URI unmodified.

        Also handles lists of URIs
        """

        if uri is None:
            return None

        # convert everything to lists
        multiple = not isinstance(uri, basestring)
        uris = uri if multiple else [uri]

        # handle all passed URIs
        converted = []
        for one_uri in uris:
            try:
                # hopefully /api/v1/<resource_name>/<pk>/
                converted.append(int(one_uri.split('/')[-2]))
            except (IndexError, ValueError):
                raise ValueError(
                    "URI %s could not be converted to PK integer." % one_uri)

        # convert back to original format
        return converted if multiple else converted[0]
