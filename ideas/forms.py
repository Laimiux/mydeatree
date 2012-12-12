from django import forms
from django.forms import ModelForm
from ideas.models import Category, Idea

class IdeaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")  
        super(IdeaForm, self).__init__(*args, **kwargs)
        
        self.fields['title'].required = True
        self.fields['title'].max_length = 30
        self.fields['title'].error_messages = {'required': 'Please enter title'}
        self.fields['text'].max_length = 140
        
        self.fields['category'].required = False
              
        if user:
            self.fields['category'].queryset = Category.objects.filter(owner=user)
        
        
    def clean_text(self):
        text = self.cleaned_data['text']
        num_words = len(text)
        if num_words < 10:
            raise forms.ValidationError("Not enough characters, you need to have more than 10!")
        return text
    
    class Meta:
        model = Idea
        fields = ('title', 'text', 'category')
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