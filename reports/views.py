from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.db.models.functions import TruncMonth, TruncYear
from django.http import HttpResponse
import csv
from datetime import datetime, timedelta

from accounts.models import CustomUser
from alumni.models import AlumniProfile
from events.models import Event, EventRegistration
from jobs.models import Job, JobReferral
from donations.models import Donation, Sponsorship


# ─── Admin Reports Dashboard ──────────────────────────────────────────────────

@login_required
def reports_dashboard_view(request):
    """Main reports dashboard with overview stats and charts."""
    if not request.user.is_admin_role:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    # Alumni stats
    total_alumni = CustomUser.objects.filter(role=CustomUser.Role.ALUMNI, is_approved=True).count()
    pending_alumni = CustomUser.objects.filter(role=CustomUser.Role.ALUMNI, is_approved=False).count()
    
    # Alumni by batch year
    alumni_by_batch = AlumniProfile.objects.filter(
        batch_year__isnull=False
    ).values('batch_year').annotate(count=Count('id')).order_by('batch_year')
    
    # Alumni by department
    alumni_by_dept = AlumniProfile.objects.filter(
        department__isnull=False
    ).exclude(department='').values('department').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Alumni by city
    alumni_by_city = AlumniProfile.objects.filter(
        city__isnull=False
    ).exclude(city='').values('city').annotate(
        count=Count('id')
    ).order_by('-count')[:10]

    # Event stats
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(event_date__gte=datetime.now()).count()
    total_registrations = EventRegistration.objects.count()
    
    # Events by type
    events_by_type = Event.objects.values('event_type').annotate(
        count=Count('id')
    ).order_by('-count')

    # Job stats
    total_jobs = Job.objects.count()
    active_jobs = Job.objects.filter(is_active=True).count()
    total_referrals = JobReferral.objects.count()
    
    # Jobs by type
    jobs_by_type = Job.objects.values('job_type').annotate(
        count=Count('id')
    ).order_by('-count')

    # Donation stats
    total_donations_amount = Donation.objects.filter(
        payment_status=Donation.PaymentStatus.COMPLETED
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    total_donations_count = Donation.objects.filter(
        payment_status=Donation.PaymentStatus.COMPLETED
    ).count()
    
    total_donors = Donation.objects.filter(
        payment_status=Donation.PaymentStatus.COMPLETED
    ).values('donor').distinct().count()
    
    # Donations by month (last 6 months)
    six_months_ago = datetime.now() - timedelta(days=180)
    donations_by_month = Donation.objects.filter(
        payment_status=Donation.PaymentStatus.COMPLETED,
        donated_at__gte=six_months_ago
    ).annotate(
        month=TruncMonth('donated_at')
    ).values('month').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('month')

    # Sponsorship stats
    total_sponsorships = Sponsorship.objects.filter(is_active=True).count()
    total_sponsorship_amount = Sponsorship.objects.filter(
        is_active=True
    ).aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'total_alumni': total_alumni,
        'pending_alumni': pending_alumni,
        'alumni_by_batch': alumni_by_batch,
        'alumni_by_dept': alumni_by_dept,
        'alumni_by_city': alumni_by_city,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'total_registrations': total_registrations,
        'events_by_type': events_by_type,
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'total_referrals': total_referrals,
        'jobs_by_type': jobs_by_type,
        'total_donations_amount': total_donations_amount,
        'total_donations_count': total_donations_count,
        'total_donors': total_donors,
        'donations_by_month': donations_by_month,
        'total_sponsorships': total_sponsorships,
        'total_sponsorship_amount': total_sponsorship_amount,
    }

    return render(request, 'reports/dashboard.html', context)


# ─── Alumni Report ────────────────────────────────────────────────────────────

@login_required
def alumni_report_view(request):
    """Detailed alumni report with filters."""
    if not request.user.is_admin_role:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    alumni = CustomUser.objects.filter(
        role=CustomUser.Role.ALUMNI, is_approved=True
    ).select_related('alumni_profile')

    # Filters
    batch_year = request.GET.get('batch_year', '')
    department = request.GET.get('department', '')
    city = request.GET.get('city', '')

    if batch_year:
        alumni = alumni.filter(alumni_profile__batch_year=batch_year)
    if department:
        alumni = alumni.filter(alumni_profile__department__icontains=department)
    if city:
        alumni = alumni.filter(alumni_profile__city__icontains=city)

    # Get filter options
    batch_years = sorted(set(
        p.batch_year for p in AlumniProfile.objects.filter(batch_year__isnull=False)
    ), reverse=True)
    departments = sorted(set(
        p.department for p in AlumniProfile.objects.filter(department__isnull=False).exclude(department='')
    ))
    cities = sorted(set(
        p.city for p in AlumniProfile.objects.filter(city__isnull=False).exclude(city='')
    ))

    context = {
        'alumni': alumni,
        'batch_years': batch_years,
        'departments': departments,
        'cities': cities,
        'selected_batch': batch_year,
        'selected_department': department,
        'selected_city': city,
    }

    return render(request, 'reports/alumni_report.html', context)


# ─── Export Alumni CSV ────────────────────────────────────────────────────────

@login_required
def export_alumni_csv(request):
    """Export alumni data to CSV."""
    if not request.user.is_admin_role:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="alumni_report.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Name', 'Email', 'Phone', 'Batch Year', 'Department', 'Degree',
        'Current Company', 'Designation', 'Industry', 'City', 'State', 'Country'
    ])

    alumni = CustomUser.objects.filter(
        role=CustomUser.Role.ALUMNI, is_approved=True
    ).select_related('alumni_profile')

    for alum in alumni:
        profile = alum.alumni_profile
        writer.writerow([
            alum.get_full_name(),
            alum.email,
            alum.phone,
            profile.batch_year or '',
            profile.department or '',
            profile.degree or '',
            profile.current_company or '',
            profile.designation or '',
            profile.industry or '',
            profile.city or '',
            profile.state or '',
            profile.country or '',
        ])

    return response


# ─── Donation Report ──────────────────────────────────────────────────────────

@login_required
def donation_report_view(request):
    """Detailed donation report."""
    if not request.user.is_admin_role:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    donations = Donation.objects.filter(
        payment_status=Donation.PaymentStatus.COMPLETED
    ).select_related('donor').order_by('-donated_at')

    # Stats
    total_amount = donations.aggregate(total=Sum('amount'))['total'] or 0
    total_count = donations.count()
    avg_donation = total_amount / total_count if total_count > 0 else 0

    # By type
    by_type = donations.values('donation_type').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')

    context = {
        'donations': donations,
        'total_amount': total_amount,
        'total_count': total_count,
        'avg_donation': avg_donation,
        'by_type': by_type,
    }

    return render(request, 'reports/donation_report.html', context)


# ─── Event Report ─────────────────────────────────────────────────────────────

@login_required
def event_report_view(request):
    """Detailed event report with registration stats."""
    if not request.user.is_admin_role:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    events = Event.objects.annotate(
        registration_count=Count('registrations')
    ).order_by('-event_date')

    context = {
        'events': events,
    }

    return render(request, 'reports/event_report.html', context)


# ─── Job Report ───────────────────────────────────────────────────────────────

@login_required
def job_report_view(request):
    """Detailed job report with referral stats."""
    if not request.user.is_admin_role:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    jobs = Job.objects.annotate(
        referral_count=Count('referrals')
    ).order_by('-created_at')

    context = {
        'jobs': jobs,
    }

    return render(request, 'reports/job_report.html', context)
