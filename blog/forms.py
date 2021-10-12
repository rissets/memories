from django import forms
from mptt.forms import TreeNodeChoiceField

from .models import Category, Comment


class CommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update({'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False
    class Meta:
        model = Comment
        fields = ('name', 'parent', 'email', 'content')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'col-sm-12', 'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'col-sm-12', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
    
    
class PostSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['c'].widget.attrs.update({'class': 'custom-select mr-2'})
        self.fields['c'].label = ''
        self.fields['q'].widget.attrs.update({'data-toggle': 'dropdown'})
        self.fields['q'].widget.attrs.update({'autocomplete': 'off'})
        
    query_category = Category.objects.all().order_by('name')
    q = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control dropdown-toggle menudd'}), label='')

    c = forms.ModelChoiceField(query_category, required=False)


