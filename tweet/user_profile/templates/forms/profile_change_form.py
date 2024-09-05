from django import forms

class ProfileChangeForm(forms.Form):
    display_name = forms.CharField(required=False, max_length=18)
    bio = forms.CharField(required=False, max_length=80)
    location = forms.CharField(required=False, max_length=20)
    date_of_birth = forms.DateField(required=False)
