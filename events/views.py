from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Event, EventRegistration
from .forms import EventForm


# ─── Event List ───────────────────────────────────────────────────────────────

@login_required
def event_list_view(request):
    """All active events. Alumni view; admin sees all including inactive."""
    if request.user.is_admin_role:
        events = Event.objects.all().order_by('-event_date')
    else:
        events = Event.objects.filter(is_active=True).order_by('-event_date')

    # Mark which events the current user has registered for
    registered_ids = set(
        EventRegistration.objects.filter(alumni=request.user).values_list('event_id', flat=True)
    )

    return render(request, 'events/event_list.html', {
        'events': events,
        'registered_ids': registered_ids,
    })


# ─── Event Detail ─────────────────────────────────────────────────────────────

@login_required
def event_detail_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    is_registered = EventRegistration.objects.filter(
        event=event, alumni=request.user
    ).exists()
    registrations_count = event.registrations.count()

    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_registered': is_registered,
        'registrations_count': registrations_count,
    })


# ─── Register for Event ───────────────────────────────────────────────────────

@login_required
def event_register_view(request, event_id):
    """Alumni registers for an event."""
    event = get_object_or_404(Event, id=event_id, is_active=True)

    if not event.registration_open:
        messages.warning(request, 'Registration for this event is closed.')
        return redirect('event_detail', event_id=event_id)

    _, created = EventRegistration.objects.get_or_create(event=event, alumni=request.user)
    if created:
        messages.success(request, f'You have registered for "{event.title}"!')
    else:
        messages.info(request, 'You are already registered for this event.')

    return redirect('event_detail', event_id=event_id)


# ─── Admin: Create Event ──────────────────────────────────────────────────────

@login_required
def event_create_view(request):
    if not request.user.is_admin_role:
        messages.error(request, 'Access denied.')
        return redirect('event_list')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            
            # Send email notification to all approved alumni
            if event.is_active:
                from accounts.models import CustomUser
                from alumni_management.email_utils import send_event_notification
                
                alumni_emails = list(
                    CustomUser.objects.filter(
                        role=CustomUser.Role.ALUMNI,
                        is_approved=True
                    ).values_list('email', flat=True)
                )
                
                try:
                    sent_count = send_event_notification(event, alumni_emails)
                    if sent_count > 0:
                        messages.success(
                            request,
                            f'Event "{event.title}" created and {sent_count} notification(s) sent!'
                        )
                    else:
                        messages.success(request, f'Event "{event.title}" created successfully!')
                except Exception:
                    messages.success(request, f'Event "{event.title}" created successfully!')
            else:
                messages.success(request, f'Event "{event.title}" created successfully!')
            
            return redirect('event_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = EventForm()

    return render(request, 'events/event_form.html', {'form': form, 'action': 'Create'})


# ─── Admin: Edit Event ────────────────────────────────────────────────────────

@login_required
def event_edit_view(request, event_id):
    if not request.user.is_admin_role:
        messages.error(request, 'Access denied.')
        return redirect('event_list')

    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, f'Event "{event.title}" updated.')
            return redirect('event_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = EventForm(instance=event)

    return render(request, 'events/event_form.html', {
        'form': form,
        'action': 'Edit',
        'event': event,
    })


# ─── Admin: Delete Event ──────────────────────────────────────────────────────

@login_required
def event_delete_view(request, event_id):
    if not request.user.is_admin_role:
        messages.error(request, 'Access denied.')
        return redirect('event_list')

    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        title = event.title
        event.delete()
        messages.success(request, f'Event "{title}" deleted.')
        return redirect('event_list')

    return render(request, 'events/event_confirm_delete.html', {'event': event})
