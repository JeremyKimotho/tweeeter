from django import forms

class NewPostForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(attrs={
            'class': 'form-control custom-text-field auto-expand', 
            'placeholder': 'What is happening?!',
            'rows' : '4',
        }), max_length=240)