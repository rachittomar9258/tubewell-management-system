from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.http import JsonResponse
from django.contrib.auth import get_user_model

def debug_users(request):
    User = get_user_model()
    users = list(User.objects.values('username', 'role', 'is_staff', 'is_superuser', 'is_active'))
    return JsonResponse({'users': users, 'count': len(users)})

def debug_create_superuser(request):
    User = get_user_model()
    if not User.objects.filter(username='Rachit2').exists():
        User.objects.create_superuser(
            username='Rachit2',
            email='test@test.com',
            password='TestPass123!',
            role='admin'
        )
        return JsonResponse({'status': 'created'})
    return JsonResponse({'status': 'already exists'})

urlpatterns = [
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('tubewells/', include('tubewells.urls')),
    path('usage/', include('usage.urls')),
    path('payments/', include('payments.urls')),
    path('debug-users-temp-xyz/', debug_users),
    path('debug-create-user-temp-xyz/', debug_create_superuser),
]