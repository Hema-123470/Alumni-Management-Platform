from django.contrib import admin
from .models import Job, JobReferral


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display  = ['title', 'company', 'job_type', 'location', 'is_active', 'last_date', 'posted_by']
    list_filter   = ['job_type', 'is_active']
    search_fields = ['title', 'company', 'description']
    ordering      = ['-created_at']


@admin.register(JobReferral)
class JobReferralAdmin(admin.ModelAdmin):
    list_display  = ['job', 'referred_by', 'referee_name', 'referee_email', 'referred_at']
    list_filter   = ['job']
    search_fields = ['referee_name', 'referee_email', 'referred_by__email']
