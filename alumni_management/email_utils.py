"""
Email notification utilities for Alumni Management System.
Phase 3: Email notifications for events and jobs.
"""

from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from django.template.loader import render_to_string


def send_event_notification(event, recipients):
    """
    Send email notification about a new event to a list of recipients.
    
    Args:
        event: Event object
        recipients: List of email addresses
    
    Returns:
        Number of emails sent successfully
    """
    if not recipients:
        return 0

    subject = f'New Event: {event.title}'
    message = f'''
Dear Alumni,

We are excited to announce a new event:

Event: {event.title}
Type: {event.get_event_type_display()}
Date: {event.event_date.strftime("%d %B %Y at %I:%M %p")}
Venue: {event.venue or "TBA"}

{event.description[:200]}...

Register now at: http://127.0.0.1:8000/events/{event.id}/

Best regards,
Alumni Management Team
    '''.strip()

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=False,
        )
        return len(recipients)
    except Exception as e:
        print(f'Email send error: {e}')
        return 0


def send_job_notification(job, recipients):
    """
    Send email notification about a new job posting to a list of recipients.
    
    Args:
        job: Job object
        recipients: List of email addresses
    
    Returns:
        Number of emails sent successfully
    """
    if not recipients:
        return 0

    subject = f'New Job Opportunity: {job.title} at {job.company}'
    message = f'''
Dear Alumni,

A new job opportunity has been posted:

Position: {job.title}
Company: {job.company}
Type: {job.get_job_type_display()}
Location: {job.location or "Remote"}
Salary: {job.salary_range or "Not specified"}

{job.description[:200]}...

View details and refer candidates at: http://127.0.0.1:8000/jobs/{job.id}/

Best regards,
Alumni Management Team
    '''.strip()

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=False,
        )
        return len(recipients)
    except Exception as e:
        print(f'Email send error: {e}')
        return 0


def send_approval_notification(user):
    """
    Send email notification when an alumni account is approved.
    
    Args:
        user: CustomUser object
    
    Returns:
        True if sent successfully, False otherwise
    """
    subject = 'Your Alumni Account Has Been Approved!'
    message = f'''
Dear {user.get_full_name()},

Great news! Your alumni account has been approved by the administrator.

You can now log in and access all features:
- Update your profile
- Register for events
- Browse job postings
- Refer candidates
- Make donations

Login at: http://127.0.0.1:8000/login/

Welcome to the alumni community!

Best regards,
Alumni Management Team
    '''.strip()

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f'Email send error: {e}')
        return False


def send_bulk_notification(subject, message, recipients):
    """
    Send a custom bulk email to multiple recipients.
    
    Args:
        subject: Email subject
        message: Email body
        recipients: List of email addresses
    
    Returns:
        Number of emails sent successfully
    """
    if not recipients:
        return 0

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=False,
        )
        return len(recipients)
    except Exception as e:
        print(f'Email send error: {e}')
        return 0
