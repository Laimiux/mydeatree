from django.contrib import admin
from contributors.models import ObjectContributor

class ObjectContributorAdmin(admin.ModelAdmin):
    list_display = ('contributor', 'content_type', 'object_id', 'content_object')
  
admin.site.register(ObjectContributor, ObjectContributorAdmin)