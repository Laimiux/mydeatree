from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from friends.forms import FriendForm

from django.contrib.auth.models import User
from django.forms.util import ErrorList

def show_user_friends(request):
    current_user = request.user

    friend_list = current_user.get_profile().get_friends()
    form = FriendForm(request.POST or None)
    
    if form.is_valid():
        cd = form.cleaned_data
        # if email doesn't equal your's continue
        if current_user.email != cd['email']:
            try:
                User.objects.get(email=cd['email'])
            except User.DoesNotExist:
                form._errors["email"] = ErrorList([u'There is no user by such email!'])

        else:
            form._errors["email"] = ErrorList([u'This email address is yours. You cannot add yourself as a friend!'])
    return render_to_response('show_friends.html',{ 'friend_list' : friend_list, 'form' : form },
                               context_instance=RequestContext(request))