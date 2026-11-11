from django import forms
from .models import Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['title', 'description', 'event_type', 'venue',
                  'event_date', 'last_date_to_register', 'banner', 'is_active']
        widgets = {
            'title':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'event_type':  forms.Select(attrs={'class': 'form-select'}),
            'venue':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Venue / Online link'}),
            'event_date':  forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
            'last_date_to_register': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d',
            ),
            'banner':    forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make datetime fields use the correct input format
        self.fields['event_date'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['last_date_to_register'].input_formats = ['%Y-%m-%d']
