from django import forms
from ideas.models import Category

class IdeaForm(forms.Form):
    title = forms.CharField(max_length=30, error_messages={'required': 'Please enter title'})
    text = forms.CharField(max_length=140, widget=forms.Textarea)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    
    def clean_text(self):
        text = self.cleaned_data['text']
        num_words = len(text.split())
        if num_words < 4:
            raise forms.ValidationError("Not enough words!")
        return text
    
    
class CategoryForm(forms.Form):
    name = forms.CharField(max_length=30)
    
    def clean_name(self):
        text = self.cleaned_data['name']
        if len(text) < 4:
            raise forms.ValidationError("Category name has to be more than 3 letters") 
        return text