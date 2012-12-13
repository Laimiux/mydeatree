from django.contrib import admin
from ideas.models import Idea, Category, IdeaForm

class IdeaAdmin(admin.ModelAdmin):
    form = IdeaForm
    list_display = ('owner', 'title', 'text')
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name')
    
admin.site.register(Idea, IdeaAdmin)
admin.site.register(Category, CategoryAdmin)
