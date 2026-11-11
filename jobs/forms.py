from django import forms
from .models import Job, JobReferral


class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ['title', 'company', 'location', 'job_type', 'description',
                  'requirements', 'salary_range', 'apply_link', 'last_date', 'is_active']
        widgets = {
            'title':        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job title'}),
            'company':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company name'}),
            'location':     forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City / Remote'}),
            'job_type':     forms.Select(attrs={'class': 'form-select'}),
            'description':  forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Skills, experience...'}),
            'salary_range': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. ₹5–8 LPA'}),
            'apply_link':   forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'last_date':    forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'is_active':    forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['last_date'].input_formats = ['%Y-%m-%d']


class JobReferralForm(forms.ModelForm):

    class Meta:
        model = JobReferral
        fields = ['referee_name', 'referee_email', 'note']
        widgets = {
            'referee_name':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Referee's full name"}),
            'referee_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "Referee's email"}),
            'note':          forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional note...'}),
        }
