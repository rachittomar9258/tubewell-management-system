from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from tubewells.models import Tubewell, AuthorizedRenter
from .models import Payment
from .forms import OwnerPaymentForm


@login_required
def record_payment(request, tubewell_id, renter_id):
    tubewell = get_object_or_404(Tubewell, id=tubewell_id, owner=request.user)
    link = get_object_or_404(AuthorizedRenter, tubewell=tubewell, renter_id=renter_id, owner=request.user)
    renter = link.renter

    if request.method == 'POST':
        form = OwnerPaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            Payment.objects.create(
                tubewell=tubewell,
                paid_by=renter,
                paid_to=request.user,
                amount=amount,
                method='cash',
                status='success',
                initiated_by=request.user,
                confirmed_by=request.user,
                confirmed_at=timezone.now(),
            )
            messages.success(request, f"₹{amount} payment record ho gaya.")

    return redirect('renter_action_panel', tubewell_id=tubewell.id, renter_id=renter.id)