from django.contrib import admin
from favorites.models import FavoriteItem

class FavoriteItemAdmin(admin.ModelAdmin):
    list_display = ('user','content_type', 'object_id', 'content_object')
    
  
admin.site.register(FavoriteItem, FavoriteItemAdmin)