from django.contrib import admin
from favorites.models import Favorite

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'content_object')
    
  
admin.site.register(Favorite, FavoriteAdmin)