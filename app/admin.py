from django.contrib import admin
from app.models import FavoriteIdeaList

class FavoriteIdeaAdmin(admin.ModelAdmin):
    list_display = ('owner', 'favorites')
    
  
admin.site.register(FavoriteIdeaList, FavoriteIdeaAdmin)

