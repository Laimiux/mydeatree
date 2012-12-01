from django.http import Http404
from ideas.models import Idea
#All the helper functions go here
def convert_to_int(id):
    try:
        object_id = int(id)
    except ValueError:
        raise Http404()
    
    return object_id
        
    