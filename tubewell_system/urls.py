from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth import get_user_model

def debug_users(request):
    User = get_user_model()
    users = list(User.objects.values('username', 'role', 'is_staff', 'is_superuser', 'is_active'))
    return JsonResponse({'users': users, 'count': len(users)})


urlpatterns = [
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('tubewells/', include('tubewells.urls')),
    path('usage/', include('usage.urls')),
    path('payments/', include('payments.urls')),
    path('debug-users-temp-xyz/', debug_users),
  ]