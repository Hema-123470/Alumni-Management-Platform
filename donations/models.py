from django.db import models
from django.conf import settings
from django.utils import timezone


class Donation(models.Model):
    """
    Donations made by alumni. Can be one-time or recurring.
    """

    class DonationType(models.TextChoices):
        ONE_TIME  = 'one_time',  'One-Time'
        MONTHLY   = 'monthly',   'Monthly'
        YEARLY    = 'yearly',    'Yearly'

    class PaymentStatus(models.TextChoices):
        PENDING   = 'pending',   'Pending'
        COMPLETED = 'completed', 'Completed'
        FAILED    = 'failed',    'Failed'

    donor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='donations',
    )
    
    # Donation details
    amount          = models.DecimalField(max_digits=10, decimal_places=2)
    donation_type   = models.CharField(max_length=20, choices=DonationType.choices, default=DonationType.ONE_TIME)
    purpose         = models.CharField(max_length=200, blank=True, help_text='e.g., Scholarship Fund, Infrastructure')
    message         = models.TextField(blank=True, max_length=500)
    
    # Payment info
    payment_method  = models.CharField(max_length=50, blank=True, help_text='e.g., Credit Card, UPI, Bank Transfer')
    transaction_id  = models.CharField(max_length=100, blank=True)
    payment_status  = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    
    # Anonymous donation option
    is_anonymous    = models.BooleanField(default=False)
    
    # Timestamps
    donated_at      = models.DateTimeField(default=timezone.now)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-donated_at']
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'

    def __str__(self):
        donor_name = 'Anonymous' if self.is_anonymous else self.donor.get_full_name()
        return f'₹{self.amount} by {donor_name} on {self.donated_at.strftime("%d %b %Y")}'

    @property
    def donor_display_name(self):
        """Return donor name or 'Anonymous'."""
        if self.is_anonymous:
            return 'Anonymous Donor'
        return self.donor.get_full_name() if self.donor else 'Unknown'


class Sponsorship(models.Model):
    """
    Corporate or individual sponsorships for events or initiatives.
    """

    class SponsorshipType(models.TextChoices):
        PLATINUM = 'platinum', 'Platinum'
        GOLD     = 'gold',     'Gold'
        SILVER   = 'silver',   'Silver'
        BRONZE   = 'bronze',   'Bronze'

    sponsor_name    = models.CharField(max_length=200)
    sponsor_email   = models.EmailField()
    sponsor_phone   = models.CharField(max_length=15, blank=True)
    company         = models.CharField(max_length=200, blank=True)
    
    sponsorship_type = models.CharField(max_length=20, choices=SponsorshipType.choices, default=SponsorshipType.BRONZE)
    amount          = models.DecimalField(max_digits=10, decimal_places=2)
    purpose         = models.CharField(max_length=200, blank=True)
    description     = models.TextField(blank=True)
    
    logo            = models.ImageField(upload_to='sponsor_logos/', blank=True, null=True)
    website_url     = models.URLField(blank=True)
    
    is_active       = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Sponsorship'
        verbose_name_plural = 'Sponsorships'

    def __str__(self):
        return f'{self.sponsor_name} — {self.get_sponsorship_type_display()} (₹{self.amount})'
