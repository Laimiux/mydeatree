from django.contrib import admin
from ideas.models import Idea, Category, IdeaForm

class IdeaAdmin(admin.ModelAdmin):
    form = IdeaForm
    list_display = ('id', 'owner', 'title','parent', 'public', 'modified_date', 'created_date')
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name')
    
admin.site.register(Idea, IdeaAdmin)
admin.site.register(Category, CategoryAdmin)
