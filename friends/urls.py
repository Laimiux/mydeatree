from django.conf.urls.defaults import *

from friends.views import *

from ideas.views import requires_login

urlpatterns = patterns('',
    (r'^friends/$', requires_login(show_user_friends)),
)
