from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.core.mail import send_mail
from django.conf import settings

from .models import Donation, Sponsorship
from .forms import DonationForm, SponsorshipForm


# ─── Donation List ────────────────────────────────────────────────────────────

@login_required
def donation_list_view(request):
    """List all donations. Admin sees all; alumni see only their own."""
    if request.user.is_admin_role:
        donations = Donation.objects.select_related('donor').all()
        total_amount = donations.filter(payment_status=Donation.PaymentStatus.COMPLETED).aggregate(
            total=Sum('amount')
        )['total'] or 0
        total_donors = donations.filter(payment_status=Donation.PaymentStatus.COMPLETED).values('donor').distinct().count()
    else:
        donations = Donation.objects.filter(donor=request.user)
        total_amount = donations.filter(payment_status=Donation.PaymentStatus.COMPLETED).aggregate(
            total=Sum('amount')
        )['total'] or 0
        total_donors = 1 if donations.exists() else 0

    return render(request, 'donations/donation_list.html', {
        'donations': donations,
        'total_amount': total_amount,
        'total_donors': total_donors,
    })


# ─── Make Donation ────────────────────────────────────────────────────────────

@login_required
def make_donation_view(request):
    """Alumni makes a donation."""
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.payment_status = Donation.PaymentStatus.COMPLETED  # Simulate payment success
            donation.transaction_id = f'TXN{donation.donated_at.strftime("%Y%m%d%H%M%S")}'
            donation.save()

            # Send email notification
            try:
                send_mail(
                    subject='Thank You for Your Donation!',
                    message=f'Dear {request.user.get_full_name()},\n\n'
                            f'Thank you for your generous donation of ₹{donation.amount}.\n'
                            f'Transaction ID: {donation.transaction_id}\n\n'
                            f'Your support helps us continue our mission.\n\n'
                            f'Best regards,\nAlumni Management Team',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[request.user.email],
                    fail_silently=True,
                )
            except Exception:
                pass  # Email failure shouldn't block donation

            messages.success(request, f'Thank you! Your donation of ₹{donation.amount} has been received.')
            return redirect('donation_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = DonationForm()

    return render(request, 'donations/make_donation.html', {'form': form})


# ─── Sponsorship List ─────────────────────────────────────────────────────────

@login_required
def sponsorship_list_view(request):
    """List all sponsorships."""
    if request.user.is_admin_role:
        sponsorships = Sponsorship.objects.all()
    else:
        sponsorships = Sponsorship.objects.filter(is_active=True)

    return render(request, 'donations/sponsorship_list.html', {
        'sponsorships': sponsorships,
    })


# ─── Admin: Create Sponsorship ────────────────────────────────────────────────

@login_required
def sponsorship_create_view(request):
    if not request.user.is_admin_role:
        messages.error(request, 'Access denied.')
        return redirect('sponsorship_list')

    if request.method == 'POST':
        form = SponsorshipForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sponsorship added successfully!')
            return redirect('sponsorship_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = SponsorshipForm()

    return render(request, 'donations/sponsorship_form.html', {'form': form, 'action': 'Add'})


# ─── Admin: Edit Sponsorship ──────────────────────────────────────────────────

@login_required
def sponsorship_edit_view(request, sponsorship_id):
    if not request.user.is_admin_role:
        messages.error(request, 'Access denied.')
        return redirect('sponsorship_list')

    sponsorship = get_object_or_404(Sponsorship, id=sponsorship_id)

    if request.method == 'POST':
        form = SponsorshipForm(request.POST, request.FILES, instance=sponsorship)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sponsorship updated.')
            return redirect('sponsorship_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = SponsorshipForm(instance=sponsorship)

    return render(request, 'donations/sponsorship_form.html', {
        'form': form,
        'action': 'Edit',
        'sponsorship': sponsorship,
    })


# ─── Admin: Delete Sponsorship ────────────────────────────────────────────────

@login_required
def sponsorship_delete_view(request, sponsorship_id):
    if not request.user.is_admin_role:
        messages.error(request, 'Access denied.')
        return redirect('sponsorship_list')

    sponsorship = get_object_or_404(Sponsorship, id=sponsorship_id)
    if request.method == 'POST':
        name = sponsorship.sponsor_name
        sponsorship.delete()
        messages.success(request, f'Sponsorship from {name} deleted.')
        return redirect('sponsorship_list')

    return render(request, 'donations/sponsorship_confirm_delete.html', {'sponsorship': sponsorship})
