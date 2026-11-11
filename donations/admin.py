from django.contrib import admin
from .models import Donation, Sponsorship


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor_display_name', 'amount', 'donation_type', 'purpose', 
                    'payment_status', 'donated_at']
    list_filter = ['donation_type', 'payment_status', 'is_anonymous']
    search_fields = ['donor__email', 'donor__first_name', 'donor__last_name', 'purpose']
    ordering = ['-donated_at']
    
    def donor_display_name(self, obj):
        return obj.donor_display_name
    donor_display_name.short_description = 'Donor'


@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    list_display = ['sponsor_name', 'company', 'sponsorship_type', 'amount', 
                    'is_active', 'created_at']
    list_filter = ['sponsorship_type', 'is_active']
    search_fields = ['sponsor_name', 'company', 'sponsor_email']
    ordering = ['-created_at']
