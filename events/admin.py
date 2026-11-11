from django.contrib import admin
from .models import Event, EventRegistration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display  = ['title', 'event_type', 'event_date', 'venue', 'is_active', 'created_by']
    list_filter   = ['event_type', 'is_active']
    search_fields = ['title', 'description', 'venue']
    ordering      = ['-event_date']


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display  = ['event', 'alumni', 'registered_at']
    list_filter   = ['event']
    search_fields = ['alumni__email', 'event__title']
