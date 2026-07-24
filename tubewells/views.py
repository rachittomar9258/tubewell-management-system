from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Tubewell, AuthorizedRenter
from .forms import TubewellForm, AddRenterForm
from .forms import EditRenterForm
from django.views.decorators.cache import never_cache

User = get_user_model()

@never_cache
@login_required
def owner_dashboard(request):
    if request.user.role != 'owner':
        return redirect('dashboard_redirect')
    tubewells = Tubewell.objects.filter(owner=request.user, is_active=True)
    inactive_tubewells = Tubewell.objects.filter(owner=request.user, is_active=False)
    return render(request, 'tubewells/owner_dashboard.html', {'tubewells': tubewells, 'inactive_tubewells': inactive_tubewells})

@never_cache
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

@never_cache
@login_required
def edit_tubewell(request, tubewell_id):
    tubewell = get_object_or_404(Tubewell, id=tubewell_id, owner=request.user)

    if request.method == 'POST':
        form = TubewellForm(request.POST, instance=tubewell)
        if form.is_valid():
            form.save()
            messages.success(request, "Tubewell details update ho gaye.")
            return redirect('tubewell_detail', tubewell_id=tubewell.id)
    else:
        form = TubewellForm(instance=tubewell)

    return render(request, 'tubewells/edit_tubewell.html', {
        'form': form,
        'tubewell': tubewell,
    })

@never_cache
@login_required
def tubewell_detail(request, tubewell_id):
    tubewell = get_object_or_404(Tubewell, id=tubewell_id, owner=request.user)
    authorized_renters = AuthorizedRenter.objects.filter(tubewell=tubewell, is_active=True)
    inactive_renters = AuthorizedRenter.objects.filter(tubewell=tubewell, is_active=False)

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
    
            link, link_created = AuthorizedRenter.objects.get_or_create(
                owner=request.user,
                renter=renter,
                tubewell=tubewell,
                defaults={'is_active': True}
            )
            if not link_created and not link.is_active:
                link.is_active = True
                link.save() 
            return redirect('tubewell_detail', tubewell_id=tubewell.id)
    else:
        form = AddRenterForm()

    return render(request, 'tubewells/tubewell_detail.html', {
        'tubewell': tubewell,
        'authorized_renters': authorized_renters,
        'inactive_renters': inactive_renters,
        'form': form,
    })

@never_cache
@login_required
def delete_tubewell(request, tubewell_id):
    tubewell = get_object_or_404(Tubewell, id=tubewell_id, owner=request.user)

    if request.method == 'POST':
        tubewell.is_active = False
        tubewell.save()
        messages.success(request, f"{tubewell.name} delete ho gaya.")
        return redirect('owner_dashboard')

    return render(request, 'tubewells/delete_tubewell_confirm.html', {'tubewell': tubewell})

@never_cache
@login_required
def reactivate_tubewell(request, tubewell_id):
    tubewell = get_object_or_404(Tubewell, id=tubewell_id, owner=request.user)

    if request.method == 'POST':
        tubewell.is_active = True
        tubewell.save()
        messages.success(request, f"{tubewell.name} wapas active ho gaya.")

    return redirect('owner_dashboard')

@never_cache
@login_required
def remove_renter(request, tubewell_id, renter_id):
    tubewell = get_object_or_404(Tubewell, id=tubewell_id, owner=request.user)
    link = get_object_or_404(AuthorizedRenter, tubewell=tubewell, renter_id=renter_id, owner=request.user)

    if request.method == 'POST':
        link.is_active = False
        link.save()
        messages.success(request, f"{link.renter.first_name} ko remove kar diya.")

    return redirect('tubewell_detail', tubewell_id=tubewell.id)


@never_cache
@login_required
def restore_renter(request, tubewell_id, renter_id):
    tubewell = get_object_or_404(Tubewell, id=tubewell_id, owner=request.user)
    link = get_object_or_404(AuthorizedRenter, tubewell=tubewell, renter_id=renter_id, owner=request.user)

    if request.method == 'POST':
        link.is_active = True
        link.save()
        messages.success(request, f"{link.renter.first_name} wapas add ho gaya.")

    return redirect('tubewell_detail', tubewell_id=tubewell.id)

@never_cache
@login_required
def edit_renter(request, tubewell_id, renter_id):
    tubewell = get_object_or_404(Tubewell, id=tubewell_id, owner=request.user)
    link = get_object_or_404(AuthorizedRenter, tubewell=tubewell, renter_id=renter_id, owner=request.user)
    renter = link.renter

    if request.method == 'POST':
        form = EditRenterForm(request.POST)
        if form.is_valid():
            renter.first_name = form.cleaned_data['name']
            renter.save()
            messages.success(request, "Renter ka naam update ho gaya.")
            return redirect('tubewell_detail', tubewell_id=tubewell.id)
    else:
        form = EditRenterForm(initial={'name': renter.first_name})

    return render(request, 'tubewells/edit_renter.html', {
        'form': form,
        'tubewell': tubewell,
        'renter': renter,
    })