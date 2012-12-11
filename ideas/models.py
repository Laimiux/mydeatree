from django.db import models
from django.contrib.auth.models import User
from djangotoolbox.fields import ListField
from django import forms

import datetime

    
class IdeaManager(models.Manager):
    
    def pagination_by_date(self, items_per_page, page, *args, **kwargs):
        return self.order_by('created_date').reverse()[items_per_page*(page-1):page*items_per_page]
    
    #filter(owner=current_user, parent=None).
    def title_count(self, keyword):
        return self.filter(title__icontains=keyword).count()
    
class Category(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=30)
    
    created_date = models.DateTimeField(default=datetime.datetime.today())
    modified_date = models.DateTimeField(default=datetime.datetime.today())
    
    def get_absolute_url(self):
        return "/categories/%i/" % self.id
    
    def get_del_url(self):
        return self.get_absolute_url() + "del/"
    
    def __unicode__(self):
        return self.name

class Idea(models.Model): 
    owner = models.ForeignKey(User, null=True, blank=True)
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=140) 
    parent = models.ForeignKey('self', blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True)
    
    created_date = models.DateTimeField(default=datetime.datetime.today())
    modified_date = models.DateTimeField(default=datetime.datetime.today())

    contributors = ListField(null=True, blank=True)
    
    objects = IdeaManager()
    
    
    def save(self, *args, **kwargs):
       ''' On save, update timestamps '''
       if not self.id:
            self.created_date = datetime.datetime.today()
       self.modified_date = datetime.datetime.today()
       
       if self.parent:
           self.parent.modified_date = self.modified_date
           self.parent.save()
           
       super(Idea, self).save(*args, **kwargs)
        
    def delete(self):
        children_ideas = self.idea_set.all()
        super(Idea, self).delete()     
        for child in children_ideas:
            child.delete() 
    
    def get_absolute_url(self):
        return "/idea/%i/" % self.id
    
    def get_add_url(self):
        return self.get_absolute_url() + "add/"
    
    def get_del_url(self):
        return self.get_absolute_url() + "del/"
    
    def get_edit_url(self):
        return self.get_absolute_url() + "edit/"
    
    def get_all_children(self, include_self=True):
        r = []
        if include_self:
            r.append(self)
        for c in Idea.objects.filter(parent=self):
            r.append(c.get_all_children(include_self=False))
        return r
    
    def __unicode__(self):
        return self.title
 
