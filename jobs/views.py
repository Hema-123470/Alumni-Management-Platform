from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Job, JobReferral
from .forms import JobForm, JobReferralForm


# ─── Job List ─────────────────────────────────────────────────────────────────

@login_required
def job_list_view(request):
    """All active jobs. Admin sees all including inactive."""
    if request.user.is_admin_role:
        jobs = Job.objects.all().order_by('-created_at')
    else:
        jobs = Job.objects.filter(is_active=True).order_by('-created_at')

    return render(request, 'jobs/job_list.html', {'jobs': jobs})


# ─── Job Detail ───────────────────────────────────────────────────────────────

@login_required
def job_detail_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    referral_form = JobReferralForm()
    user_referrals = JobReferral.objects.filter(job=job, referred_by=request.user)

    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'referral_form': referral_form,
        'user_referrals': user_referrals,
    })


# ─── Refer a Job ──────────────────────────────────────────────────────────────

@login_required
def job_refer_view(request, job_id):
    """Alumni submits a referral for a job posting."""
    job = get_object_or_404(Job, id=job_id, is_active=True)

    if request.method == 'POST':
        form = JobReferralForm(request.POST)
        if form.is_valid():
            referral = form.save(commit=False)
            referral.job = job
            referral.referred_by = request.user
            referral.save()
            messages.success(
                request,
                f'Referral for {referral.referee_name} submitted successfully!'
            )
            return redirect('job_detail', job_id=job_id)
        else:
            messages.error(request, 'Please fix the errors below.')
            return render(request, 'jobs/job_detail.html', {
                'job': job,
                'referral_form': form,
                'user_referrals': JobReferral.objects.filter(job=job, referred_by=request.user),
            })

    return redirect('job_detail', job_id=job_id)


# ─── Admin: Create Job ────────────────────────────────────────────────────────

@login_required
def job_create_view(request):
    if not request.user.is_admin_role:
        messages.error(request, 'Access denied.')
        return redirect('job_list')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            
            # Send email notification to all approved alumni
            if job.is_active:
                from accounts.models import CustomUser
                from alumni_management.email_utils import send_job_notification
                
                alumni_emails = list(
                    CustomUser.objects.filter(
                        role=CustomUser.Role.ALUMNI,
                        is_approved=True
                    ).values_list('email', flat=True)
                )
                
                try:
                    sent_count = send_job_notification(job, alumni_emails)
                    if sent_count > 0:
                        messages.success(
                            request,
                            f'Job "{job.title}" posted and {sent_count} notification(s) sent!'
                        )
                    else:
                        messages.success(request, f'Job "{job.title}" posted successfully!')
                except Exception:
                    messages.success(request, f'Job "{job.title}" posted successfully!')
            else:
                messages.success(request, f'Job "{job.title}" posted successfully!')
            
            return redirect('job_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = JobForm()

    return render(request, 'jobs/job_form.html', {'form': form, 'action': 'Post'})


# ─── Admin: Edit Job ──────────────────────────────────────────────────────────

@login_required
def job_edit_view(request, job_id):
    if not request.user.is_admin_role:
        messages.error(request, 'Access denied.')
        return redirect('job_list')

    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, f'Job "{job.title}" updated.')
            return redirect('job_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/job_form.html', {
        'form': form,
        'action': 'Edit',
        'job': job,
    })


# ─── Admin: Delete Job ────────────────────────────────────────────────────────

@login_required
def job_delete_view(request, job_id):
    if not request.user.is_admin_role:
        messages.error(request, 'Access denied.')
        return redirect('job_list')

    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        title = job.title
        job.delete()
        messages.success(request, f'Job "{title}" deleted.')
        return redirect('job_list')

    return render(request, 'jobs/job_confirm_delete.html', {'job': job})


# ─── Admin: View Referrals ────────────────────────────────────────────────────

@login_required
def job_referrals_view(request, job_id):
    if not request.user.is_admin_role:
        messages.error(request, 'Access denied.')
        return redirect('job_list')

    job = get_object_or_404(Job, id=job_id)
    referrals = job.referrals.select_related('referred_by').order_by('-referred_at')

    return render(request, 'jobs/job_referrals.html', {
        'job': job,
        'referrals': referrals,
    })
