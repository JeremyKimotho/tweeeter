from django import forms

class ProfileChangeForm(forms.Form):
    # display_name = forms.CharField(required=False, max_length=18)
    display_name = forms.CharField(widget=forms.Textarea(attrs={
            'class': 'form-control custom-text-field auto-expand', 
            'placeholder': 'Name',
            'rows' : '1',
        }), required=False, max_length=18)
    bio = forms.CharField(widget=forms.Textarea(attrs={
            'class': 'form-control custom-text-field auto-expand', 
            'placeholder': 'Bio',
            'rows' : '2',
        }), required=False, max_length=80)
    location = forms.CharField(widget=forms.Textarea(attrs={
            'class': 'form-control custom-text-field auto-expand', 
            'placeholder': 'Location',
            'rows' : '1',
        }), required=False, max_length=20)
    date_of_birth = forms.DateField(required=False)
