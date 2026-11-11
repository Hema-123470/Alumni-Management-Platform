from django import forms
from .models import AlumniProfile


class AlumniProfileForm(forms.ModelForm):

    class Meta:
        model = AlumniProfile
        exclude = ['user', 'updated_at']
        widgets = {
            'batch_year':       forms.Select(attrs={'class': 'form-select'}),
            'department':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Computer Science'}),
            'degree':           forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. B.Tech'}),
            'current_company':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Current employer'}),
            'designation':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Software Engineer'}),
            'industry':         forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Information Technology'}),
            'skills':           forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django, MySQL, ...'}),
            'linkedin_url':     forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/...'}),
            'city':             forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state':            forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'country':          forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'bio':              forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short bio...'}),
            'profile_picture':  forms.FileInput(attrs={'class': 'form-control'}),
        }
