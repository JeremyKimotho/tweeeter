from django import forms

class NewCommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(attrs={
            'class': 'form-control custom-text-field auto-expand', 
            'placeholder': 'Post your reply',
            'rows' : '4',
        }), max_length=240)