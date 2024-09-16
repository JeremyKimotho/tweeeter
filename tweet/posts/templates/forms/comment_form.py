from django import forms

class NewCommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(attrs={
            'class': 'form-control custom-text-field auto-expand', 
            'placeholder': 'Post your reply',
            'id': 'new-comment-form-id',
            'rows' : '2',
        }), max_length=240)
    
class NewCommentFormLite(forms.Form):
    body = forms.CharField(widget=forms.Textarea(attrs={
            'class': 'form-control custom-text-field auto-expand', 
            'placeholder': 'Post your reply',
            'id': 'new-comment-form-lite-id',
            'rows' : '1',
        }), max_length=240)