from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Tubewell, AuthorizedRenter
from .forms import TubewellForm, AddRenterForm

User = get_user_model()


@login_required
def owner_dashboard(request):
    if request.user.role != 'owner':
        return redirect('dashboard_redirect')
    tubewells = Tubewell.objects.filter(owner=request.user)
    return render(request, 'tubewells/owner_dashboard.html', {'tubewells': tubewells})


@login_required
def add_tubewell(request):
    if request.user.role != 'owner':
        return redirect('dashboard_redirect')
    if request.method == 'POST':
        form = TubewellForm(request.POST)
        if form.is_valid():
            tubewell = form.save(commit=False)
            tubewell.owner = request.user
            tubewell.save()
            return redirect('owner_dashboard')
    else:
        form = TubewellForm()
    return render(request, 'tubewells/add_tubewell.html', {'form': form})


@login_required
def tubewell_detail(request, tubewell_id):
    tubewell = get_object_or_404(Tubewell, id=tubewell_id, owner=request.user)
    authorized_renters = AuthorizedRenter.objects.filter(tubewell=tubewell)

    if request.method == 'POST':
        form = AddRenterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone_number']

            renter, created = User.objects.get_or_create(
                username=phone,
                defaults={
                    'first_name': name,
                    'phone_number': phone,
                    'role': 'renter',
                }
            )
            if created:
                renter.set_password(phone)
                renter.save()
                messages.success(
                    request,
                    f"Renter add ho gaya! Login details — Phone: {phone}, Password: {phone}"
                )
            else:
                messages.info(request, f"{name} is tubewell ke liye already authorized ho gaya.")

            AuthorizedRenter.objects.get_or_create(
                owner=request.user,
                renter=renter,
                tubewell=tubewell
            )
            return redirect('tubewell_detail', tubewell_id=tubewell.id)
    else:
        form = AddRenterForm()

    return render(request, 'tubewells/tubewell_detail.html', {
        'tubewell': tubewell,
        'authorized_renters': authorized_renters,
        'form': form,
    })