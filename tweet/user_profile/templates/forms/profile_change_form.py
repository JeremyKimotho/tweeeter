from django import forms
import datetime

YEAR = datetime.datetime.now().year

MONTH_CHOICES = [
    (1, 'January'),
    (2, 'February'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December'),
]

YEAR_CHOICES = [(YEAR - i, YEAR - i) for i in range(0, 100)]
DAY_CHOICES = [(i, i) for i in range(1,31)]



class ProfileChangeForm(forms.Form):
    # display_name = forms.CharField(required=False, max_length=18)
    display_name = forms.CharField(widget=forms.Textarea(attrs={
            'class': 'form-control custom-text-field auto-expand', 
            'placeholder': 'Name',
            'id': 'p-change-form-name',
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
            'id': 'p-change-form-location',
            'rows' : '1',
        }), required=False, max_length=20, help_text='You\'re a makende')
    day = forms.ChoiceField(choices=DAY_CHOICES, label="Day")
    month = forms.ChoiceField(choices=MONTH_CHOICES, label="Month")
    year = forms.ChoiceField(choices=YEAR_CHOICES, label="Year")

