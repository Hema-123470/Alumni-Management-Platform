from django.db import models
from django.conf import settings


class AlumniProfile(models.Model):
    """
    Extended profile for alumni users.
    One-to-one with CustomUser; created/updated by the alumni themselves.
    """

    BATCH_YEARS = [(y, str(y)) for y in range(1990, 2030)]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='alumni_profile',
    )

    # Academic info
    batch_year      = models.IntegerField(choices=BATCH_YEARS, null=True, blank=True)
    department      = models.CharField(max_length=100, blank=True)
    degree          = models.CharField(max_length=100, blank=True)

    # Professional info
    current_company = models.CharField(max_length=150, blank=True)
    designation     = models.CharField(max_length=150, blank=True)
    industry        = models.CharField(max_length=100, blank=True)
    skills          = models.TextField(blank=True, help_text='Comma-separated skills')
    linkedin_url    = models.URLField(blank=True)

    # Personal info
    city            = models.CharField(max_length=100, blank=True)
    state           = models.CharField(max_length=100, blank=True)
    country         = models.CharField(max_length=100, blank=True, default='India')
    bio             = models.TextField(blank=True, max_length=500)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Alumni Profile'
        verbose_name_plural = 'Alumni Profiles'

    def __str__(self):
        return f'{self.user.get_full_name()} — {self.batch_year or "N/A"}'

    def get_skills_list(self):
        """Return skills as a cleaned list."""
        if self.skills:
            return [s.strip() for s in self.skills.split(',') if s.strip()]
        return []
