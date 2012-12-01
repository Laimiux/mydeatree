from django.conf.urls.defaults import *

from contactus.views import contact_us

urlpatterns = patterns('',
    (r'^contact/$', 'contactus.views.contact_us'),
    (r'^contact/thanks/$', 'contactus.views.thank_you'),
    )
