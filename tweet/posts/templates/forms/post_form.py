from django import forms

class NewPostForm(forms.Form):
    body = forms.CharField(label="Your post...", max_length=240)