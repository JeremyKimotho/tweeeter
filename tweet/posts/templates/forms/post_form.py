from django import forms

class NewPostForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(attrs={
            'class': 'form-control custom-text-field auto-expand', 
            'placeholder': 'What is happening?!',
            'id': 'new-post-form-id',
            'rows' : '4',
        }), max_length=240)
    
class NewPostFormLite(forms.Form):
    body = forms.CharField(widget=forms.Textarea(attrs={
            'class': 'form-control custom-text-field auto-expand', 
            'placeholder': 'What is happening?!',
            'id': 'new-post-form-lite-id',
            'rows' : '1',
        }), max_length=240)