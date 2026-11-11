from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models

from .models import AlumniProfile
from .forms import AlumniProfileForm
from accounts.models import CustomUser


# ─── My Profile ──────────────────────────────────────────────────────────────

@login_required
def my_profile_view(request):
    """View and edit the logged-in alumni's own profile."""
    profile, created = AlumniProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = AlumniProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('my_profile')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = AlumniProfileForm(instance=profile)

    return render(request, 'alumni/my_profile.html', {'form': form, 'profile': profile})


# ─── View Any Alumni Profile ──────────────────────────────────────────────────

@login_required
def view_profile_view(request, user_id):
    """View another alumni's profile (read-only)."""
    alumni_user = get_object_or_404(
        CustomUser,
        id=user_id,
        role=CustomUser.Role.ALUMNI,
        is_approved=True,
    )
    profile, _ = AlumniProfile.objects.get_or_create(user=alumni_user)
    return render(request, 'alumni/view_profile.html', {
        'alumni_user': alumni_user,
        'profile': profile,
    })


# ─── Alumni List (Admin only) ─────────────────────────────────────────────────

@login_required
def alumni_list_view(request):
    """Admin view: list all approved alumni with search and filter."""
    if not request.user.is_admin_role:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    alumni = CustomUser.objects.filter(
        role=CustomUser.Role.ALUMNI, is_approved=True
    ).select_related('alumni_profile').order_by('-date_joined')

    # Search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        alumni = alumni.filter(
            models.Q(first_name__icontains=search_query) |
            models.Q(last_name__icontains=search_query) |
            models.Q(email__icontains=search_query) |
            models.Q(alumni_profile__current_company__icontains=search_query) |
            models.Q(alumni_profile__skills__icontains=search_query) |
            models.Q(alumni_profile__city__icontains=search_query)
        )

    # Filter by batch year
    batch_year = request.GET.get('batch_year', '').strip()
    if batch_year:
        alumni = alumni.filter(alumni_profile__batch_year=batch_year)

    # Filter by department
    department = request.GET.get('department', '').strip()
    if department:
        alumni = alumni.filter(alumni_profile__department__icontains=department)

    # Filter by city
    city = request.GET.get('city', '').strip()
    if city:
        alumni = alumni.filter(alumni_profile__city__icontains=city)

    # Get unique values for filters
    all_alumni = CustomUser.objects.filter(
        role=CustomUser.Role.ALUMNI, is_approved=True
    ).select_related('alumni_profile')
    
    batch_years = sorted(set(
        p.batch_year for p in AlumniProfile.objects.filter(batch_year__isnull=False)
    ), reverse=True)
    
    departments = sorted(set(
        p.department for p in AlumniProfile.objects.filter(department__isnull=False).exclude(department='')
    ))
    
    cities = sorted(set(
        p.city for p in AlumniProfile.objects.filter(city__isnull=False).exclude(city='')
    ))

    return render(request, 'alumni/alumni_list.html', {
        'alumni': alumni,
        'search_query': search_query,
        'batch_years': batch_years,
        'departments': departments,
        'cities': cities,
        'selected_batch': batch_year,
        'selected_department': department,
        'selected_city': city,
    })
