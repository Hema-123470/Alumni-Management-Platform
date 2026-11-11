from django.db import models
from django.conf import settings
from django.utils import timezone


class Event(models.Model):
    """
    Events created by admins. Alumni can view and register.
    """

    class EventType(models.TextChoices):
        SEMINAR    = 'seminar',    'Seminar'
        WORKSHOP   = 'workshop',   'Workshop'
        REUNION    = 'reunion',    'Reunion'
        WEBINAR    = 'webinar',    'Webinar'
        NETWORKING = 'networking', 'Networking'
        OTHER      = 'other',      'Other'

    title       = models.CharField(max_length=200)
    description = models.TextField()
    event_type  = models.CharField(max_length=20, choices=EventType.choices, default=EventType.OTHER)
    venue       = models.CharField(max_length=200, blank=True)
    event_date  = models.DateTimeField()
    last_date_to_register = models.DateField(null=True, blank=True)
    banner      = models.ImageField(upload_to='event_banners/', blank=True, null=True)
    is_active   = models.BooleanField(default=True)

    created_by  = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_events',
    )
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-event_date']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        return self.event_date >= timezone.now()

    @property
    def registration_open(self):
        if self.last_date_to_register:
            return self.last_date_to_register >= timezone.now().date()
        return self.is_upcoming


class EventRegistration(models.Model):
    """Tracks which alumni registered for which event."""

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    alumni = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='event_registrations',
    )
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'alumni')
        verbose_name = 'Event Registration'

    def __str__(self):
        return f'{self.alumni.get_full_name()} → {self.event.title}'
