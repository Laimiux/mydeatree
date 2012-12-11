from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def show_user_friends(request):
    current_user = request.user

    friend_list = current_user.get_profile().get_friends()
    
    
    return render_to_response('show_friends.html',{ 'friend_list' : friend_list }, context_instance=RequestContext(request))