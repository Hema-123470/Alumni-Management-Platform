from django import forms
from .models import Donation, Sponsorship


class DonationForm(forms.ModelForm):

    class Meta:
        model = Donation
        fields = ['amount', 'donation_type', 'purpose', 'message', 
                  'payment_method', 'is_anonymous']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount',
                'min': '1',
                'step': '0.01',
            }),
            'donation_type': forms.Select(attrs={'class': 'form-select'}),
            'purpose': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Scholarship Fund, Infrastructure Development',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional message...',
            }),
            'payment_method': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Credit Card, UPI, Bank Transfer',
            }),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SponsorshipForm(forms.ModelForm):

    class Meta:
        model = Sponsorship
        fields = ['sponsor_name', 'sponsor_email', 'sponsor_phone', 'company',
                  'sponsorship_type', 'amount', 'purpose', 'description',
                  'logo', 'website_url', 'is_active']
        widgets = {
            'sponsor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sponsor name'}),
            'sponsor_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'sponsor_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company name'}),
            'sponsorship_type': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'step': '0.01'}),
            'purpose': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Purpose'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'website_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
