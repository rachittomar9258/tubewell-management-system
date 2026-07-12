from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from tubewells.models import Tubewell, AuthorizedRenter
from .models import UsageRecord
from .utils import notify_user, calculate_balance
from payments.models import Payment
from payments.forms import OwnerPaymentForm


@login_required
def renter_action_panel(request, tubewell_id, renter_id):
    tubewell = get_object_or_404(Tubewell, id=tubewell_id, owner=request.user)
    authorized = get_object_or_404(
        AuthorizedRenter, tubewell=tubewell, renter_id=renter_id, owner=request.user
    )
    renter = authorized.renter

    running_record = UsageRecord.objects.filter(
        tubewell=tubewell, used_by=renter, status='running'
    ).first()

    usage_records = UsageRecord.objects.filter(
        tubewell=tubewell, used_by=renter
    ).order_by('-created_at')

    balance = calculate_balance(request.user, renter, tubewell)
    payments = Payment.objects.filter(tubewell=tubewell, paid_by=renter).order_by('-paid_at')
    payment_form = OwnerPaymentForm()

    return render(request, 'usage/renter_action_panel.html', {
        'tubewell': tubewell,
        'renter': renter,
        'running_record': running_record,
        'usage_records': usage_records,
        'balance': balance,
        'payments': payments,
        'payment_form': payment_form,
    })


@login_required
def start_usage(request, tubewell_id, renter_id):
    tubewell = get_object_or_404(Tubewell, id=tubewell_id, owner=request.user)
    authorized = get_object_or_404(
        AuthorizedRenter, tubewell=tubewell, renter_id=renter_id, owner=request.user
    )
    renter = authorized.renter

    already_running = UsageRecord.objects.filter(
        tubewell=tubewell, used_by=renter, status='running'
    ).exists()

    if not already_running:
        UsageRecord.objects.create(
            tubewell=tubewell,
            used_by=renter,
            start_time=timezone.now(),
            status='running'
        )
        messages.success(request, f"{renter.first_name or renter.username} ke liye tubewell start ho gaya.")

    return redirect('renter_action_panel', tubewell_id=tubewell.id, renter_id=renter.id)


@login_required
def stop_usage(request, tubewell_id, renter_id):
    tubewell = get_object_or_404(Tubewell, id=tubewell_id, owner=request.user)
    authorized = get_object_or_404(
        AuthorizedRenter, tubewell=tubewell, renter_id=renter_id, owner=request.user
    )
    renter = authorized.renter

    record = UsageRecord.objects.filter(
        tubewell=tubewell, used_by=renter, status='running'
    ).first()

    if record:
        record.end_time = timezone.now()
        record.save()

        notify_user(
            renter.phone_number,
            f"Tubewell use complete hui. Time: {record.total_hours} ghante, Amount: ₹{record.amount}"
        )
        messages.success(request, f"Record ban gaya — {record.total_hours} ghante, ₹{record.amount}")

    return redirect('renter_action_panel', tubewell_id=tubewell.id, renter_id=renter.id)

@login_required
def my_usage_history(request, tubewell_id):
    if request.user.role != 'renter':
        return redirect('dashboard_redirect')

    tubewell = get_object_or_404(Tubewell, id=tubewell_id)
    is_authorized = AuthorizedRenter.objects.filter(tubewell=tubewell, renter=request.user).exists()
    if not is_authorized:
        return redirect('renter_dashboard')

    usage_records = UsageRecord.objects.filter(
        tubewell=tubewell, used_by=request.user
    ).order_by('-created_at')

    return render(request, 'usage/my_usage_history.html', {
        'tubewell': tubewell,
        'usage_records': usage_records,
    })