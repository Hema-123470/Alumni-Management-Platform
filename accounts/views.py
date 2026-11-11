from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from .forms import AlumniRegistrationForm, CustomLoginForm
from .models import CustomUser


# ─── Registration ─────────────────────────────────────────────────────────────

def register_view(request):
    """Alumni self-registration. Account is pending until admin approves."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AlumniRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Registration successful! Your account is pending admin approval. '
                'You will be able to log in once approved.'
            )
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AlumniRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


# ─── Login ────────────────────────────────────────────────────────────────────

def login_view(request):
    """Login using email + password. Alumni must be approved to access."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # Block unapproved alumni
            if user.is_alumni_role and not user.is_approved:
                messages.warning(
                    request,
                    'Your account is pending admin approval. Please wait for confirmation.'
                )
                return redirect('login')

            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = CustomLoginForm(request)

    return render(request, 'accounts/login.html', {'form': form})


# ─── Logout ───────────────────────────────────────────────────────────────────

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# ─── Dashboard ────────────────────────────────────────────────────────────────

@login_required
def dashboard_view(request):
    """
    Main dashboard. Admins see management stats; alumni see their profile summary.
    """
    from events.models import Event
    from jobs.models import Job
    from donations.models import Donation
    from django.db.models import Sum
    
    context = {'user': request.user}

    if request.user.is_admin_role:
        # Admin dashboard stats
        context['total_alumni'] = CustomUser.objects.filter(role=CustomUser.Role.ALUMNI).count()
        context['pending_approvals'] = CustomUser.objects.filter(
            role=CustomUser.Role.ALUMNI, is_approved=False
        ).count()
        context['pending_users'] = CustomUser.objects.filter(
            role=CustomUser.Role.ALUMNI, is_approved=False
        ).order_by('-date_joined')[:5]
        context['total_events'] = Event.objects.count()
        context['total_jobs'] = Job.objects.count()
        context['total_donations'] = Donation.objects.filter(
            payment_status=Donation.PaymentStatus.COMPLETED
        ).aggregate(total=Sum('amount'))['total'] or 0

    return render(request, 'accounts/dashboard.html', context)


# ─── Admin: Approve / Reject Alumni ──────────────────────────────────────────

@login_required
def pending_approvals_view(request):
    """List all alumni awaiting approval (admin only)."""
    if not request.user.is_admin_role:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    pending = CustomUser.objects.filter(
        role=CustomUser.Role.ALUMNI, is_approved=False
    ).order_by('-date_joined')

    return render(request, 'accounts/pending_approvals.html', {'pending': pending})


@login_required
def approve_user_view(request, user_id):
    """Approve an alumni account (admin only)."""
    if not request.user.is_admin_role:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    try:
        user = CustomUser.objects.get(id=user_id, role=CustomUser.Role.ALUMNI)
        user.is_approved = True
        user.save()
        
        # Send approval email notification
        from alumni_management.email_utils import send_approval_notification
        try:
            send_approval_notification(user)
        except Exception:
            pass  # Don't block approval if email fails
        
        messages.success(request, f'{user.get_full_name()} has been approved.')
    except CustomUser.DoesNotExist:
        messages.error(request, 'User not found.')

    return redirect('pending_approvals')


@login_required
def reject_user_view(request, user_id):
    """Reject (delete) an alumni registration (admin only)."""
    if not request.user.is_admin_role:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    try:
        user = CustomUser.objects.get(id=user_id, role=CustomUser.Role.ALUMNI)
        name = user.get_full_name()
        user.delete()
        messages.success(request, f'{name}\'s registration has been rejected and removed.')
    except CustomUser.DoesNotExist:
        messages.error(request, 'User not found.')

    return redirect('pending_approvals')
