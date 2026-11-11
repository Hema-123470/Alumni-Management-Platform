from django.db import models
from django.conf import settings
from django.utils import timezone


class Job(models.Model):
    """
    Job postings created by admin. Alumni can view and refer others.
    """

    class JobType(models.TextChoices):
        FULL_TIME  = 'full_time',  'Full Time'
        PART_TIME  = 'part_time',  'Part Time'
        INTERNSHIP = 'internship', 'Internship'
        CONTRACT   = 'contract',   'Contract'
        REMOTE     = 'remote',     'Remote'

    title           = models.CharField(max_length=200)
    company         = models.CharField(max_length=150)
    location        = models.CharField(max_length=150, blank=True)
    job_type        = models.CharField(max_length=20, choices=JobType.choices, default=JobType.FULL_TIME)
    description     = models.TextField()
    requirements    = models.TextField(blank=True)
    salary_range    = models.CharField(max_length=100, blank=True)
    apply_link      = models.URLField(blank=True)
    last_date       = models.DateField(null=True, blank=True)
    is_active       = models.BooleanField(default=True)

    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posted_jobs',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'

    def __str__(self):
        return f'{self.title} @ {self.company}'

    @property
    def is_open(self):
        if self.last_date:
            return self.last_date >= timezone.now().date() and self.is_active
        return self.is_active


class JobReferral(models.Model):
    """
    Alumni can refer a job to another person (name + email).
    """

    job         = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='referrals')
    referred_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='job_referrals',
    )
    referee_name  = models.CharField(max_length=100)
    referee_email = models.EmailField()
    note          = models.TextField(blank=True, max_length=300)
    referred_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Job Referral'
        verbose_name_plural = 'Job Referrals'

    def __str__(self):
        return f'{self.referred_by.get_full_name()} referred {self.referee_name} for {self.job.title}'
