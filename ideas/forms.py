from django import forms
from django.forms import ModelForm
from ideas.models import Category, Idea

# A simple contact form with four fields.
class ContributorForm(forms.Form):
    email = forms.EmailField()

    
class IdeaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop("owner", None)  
        
        super(IdeaForm, self).__init__(*args, **kwargs)
        
        self.fields['title'].required = True
        self.fields['title'].max_length = 30
        self.fields['text'].error_messages = {'required' : 'Please enter text'}
        self.fields['title'].error_messages = {'required': 'Please enter title'}
        self.fields['text'].max_length = 140
        
        #self.fields['category'].required = False
              
        #if owner:
        #    self.fields['category'].queryset = Category.objects.filter(owner=owner)
        
        
    def clean_text(self):
        text = self.cleaned_data['text']
        num_words = len(text)
        if num_words < 10:
            raise forms.ValidationError("Text needs to have more than 10 characters!")
        return text
    
    class Meta:
        model = Idea
        fields = ('title', 'text')
        widgets = {
            'text': forms.Textarea(attrs={'cols': 20, 'rows': 10, 'maxlength': 140}),
        }

    
class CategoryForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs): 
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].max_length = 30
    
    def clean_name(self):
        text = self.cleaned_data['name']
        if len(text) < 4:
            raise forms.ValidationError("Category name has to be more than 3 letters") 
        return text
    
    class Meta:
        model = Category
        fields = ['name']