from django.db import models
from django.contrib.auth.models import User
from djangotoolbox.fields import ListField
from django import forms
from django.forms import ModelForm

from django.core.urlresolvers import reverse

from friends.fields import ModelListField

import datetime

    
class IdeaManager(models.Manager):
    
    def pagination_by_date(self, items_per_page, page, *args, **kwargs):
        return self.order_by('modified_date').reverse()[items_per_page*(page-1):page*items_per_page]
    
    def get_public_ideas(self):
        return self.filter(public=True).order_by('modified_date').reverse()
    
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
    #category = models.ForeignKey(Category, blank=True, null=True)
    
    public = models.BooleanField(default=False)
    
    created_date = models.DateTimeField(default=datetime.datetime.today())
    modified_date = models.DateTimeField(default=datetime.datetime.today())

    contributors = ModelListField(models.ForeignKey(User), null=True, blank=True)
    
    objects = IdeaManager()
    
    def get_children_count(self):
        count = self.idea_set.count()    
        for idea in self.idea_set.all():
            count += idea.get_children_count()
        return count 
    
    def get_contributors(self):
        result_list = []
        if self.contributors:
            for id in self.contributors:
                result_list += User.objects.filter(pk__exact=id)
        return result_list
    
    def is_original_owner(self, user):
        if self.owner and self.owner == user:
            return True
        elif self.parent:
            return self.parent.is_original_owner(user)
        else: 
            return False
        
    def is_contributor(self, user_primary_key):
        if self.contributors and user_primary_key in self.contributors:
            return True
        elif self.parent:
            return self.parent.is_contributor(user_primary_key)
        else:
            return False
            
    def save(self, *args, **kwargs):
       ''' On save, update timestamps '''
       import sys
       print >>sys.stderr, 'Saving ' + self.title
       
       if not self.id:
            self.created_date = datetime.datetime.today()
       self.modified_date = datetime.datetime.today()
       
       
       
       if not self.parent is None:
           if hasattr(self.parent, 'modified_date'):
               self.parent.modified_date = datetime.datetime.today()
               self.parent.save()
       super(Idea, self).save(*args, **kwargs)
    
       
        
    def delete(self):
        children_ideas = self.idea_set.all()
        super(Idea, self).delete()     
        for child in children_ideas:
            child.delete() 
    
    def get_absolute_url(self):
        return reverse('show-idea', args=(self.pk,))
    
    def get_add_url(self):
        return reverse('new-children-idea', args=(self.pk,))
    
    def get_del_url(self):
        return reverse('delete-idea', args=(self.pk,))
    
    def get_edit_url(self):
        return reverse('edit-idea', args=(self.pk,))
    
    # Update the last two urls to reverse style.
    def get_add_collab_url(self):
        return self.get_absolute_url() + "collaboration/"
    
    def get_make_public_url(self):
        return self.get_absolute_url() + "make-public/"
    
    def get_all_children(self, include_self=True):
        r = []
        if include_self:
            r.append(self)
        for c in Idea.objects.filter(parent=self):
            r.append(c.get_all_children(include_self=False))
        return r
    
    def __unicode__(self):
        return self.title
    
class IdeaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(IdeaForm, self).__init__(*args, **kwargs)
        self.fields['contributors'].widget.choices = [(i.pk, i) for i in User.objects.all()]
        if self.instance.pk:
            self.fields['contributors'].initial = self.instance.contributors
    class Meta:
        model = Idea
 
