from django.contrib import admin
from ideas.models import Idea, Favorite, IdeaForm

class IdeaAdmin(admin.ModelAdmin):
    form = IdeaForm
    list_display = ('id', 'owner', 'title','parent', 'public', 'modified_date', 'created_date')
    
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'favorite_idea')
    
admin.site.register(Idea, IdeaAdmin)
admin.site.register(Favorite, FavoriteAdmin)
