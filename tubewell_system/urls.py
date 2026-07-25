from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.http import JsonResponse

urlpatterns = [
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('tubewells/', include('tubewells.urls')),
    path('usage/', include('usage.urls')),
    path('payments/', include('payments.urls')),
]