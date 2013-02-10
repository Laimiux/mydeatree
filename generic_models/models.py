from django.db import models

from django.contrib.contenttypes.models import ContentType

# Create your models here.
class SelfAwareModel(models.Model):
    class Meta:
        abstract = True
        
    def get_ct(self):
        """
        Returns the Content Type for this instance
        """
        return ContentType.objects.get_for_model(self)
    
    def get_ct_id(self):
        """
        Returns the id of the content type for this instance
        """
        return self.get_ct().pk
    
    def get_app_label(self):
        return self.get_ct().app_label
    
    def get_model_name(self):
        return self.get_ct().model
    
    