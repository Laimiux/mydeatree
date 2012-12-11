from django.contrib import admin
from friends.models import UserProfile, UserProfileForm

class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileForm
    list_display = ['user']
    
    def __init__(self, model, admin_site):
        super(UserProfileAdmin,self).__init__(model, admin_site)
     
admin.site.register(UserProfile, UserProfileAdmin)
