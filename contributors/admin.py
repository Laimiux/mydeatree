from django.contrib import admin
from contributors.models import ObjectContributor

class ObjectContributorAdmin(admin.ModelAdmin):
    list_display = ('contributor', 'idea')
  
admin.site.register(ObjectContributor, ObjectContributorAdmin)