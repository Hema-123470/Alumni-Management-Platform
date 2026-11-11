from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds role-based access: Admin or Alumni.
    Alumni accounts require admin approval before they can log in.
    """

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        ALUMNI = 'alumni', 'Alumni'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.ALUMNI,
    )

    # Alumni accounts are inactive until an admin approves them
    is_approved = models.BooleanField(
        default=False,
        help_text='Admin must approve alumni accounts before they can log in.',
    )

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)

    # Use email as the login identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.get_full_name()} ({self.role})'

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN

    @property
    def is_alumni_role(self):
        return self.role == self.Role.ALUMNI
