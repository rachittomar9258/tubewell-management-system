from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required


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
    return render(request, 'accounts/renter_dashboard.html')