from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from tubewells.models import AuthorizedRenter
from usage.utils import calculate_balance
from .forms import SignUpForm, EditProfileForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard_redirect')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def dashboard_redirect(request):
    if request.user.role == 'owner':
        return redirect('owner_dashboard')
    elif request.user.role == 'renter':
        return redirect('renter_dashboard')
    return redirect('/admin/')


@login_required
def renter_dashboard(request):
    if request.user.role != 'renter':
        return redirect('dashboard_redirect')

    authorized_links = AuthorizedRenter.objects.filter(renter=request.user, is_active=True).select_related('tubewell', 'owner')

    tubewell_data = []
    for link in authorized_links:
        balance = calculate_balance(link.owner, request.user, link.tubewell)
        tubewell_data.append({
            'tubewell': link.tubewell,
            'owner': link.owner,
            'balance': balance,
        })

    return render(request, 'accounts/renter_dashboard.html', {'tubewell_data': tubewell_data})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile update ho gayi.")
            return redirect('edit_profile')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})