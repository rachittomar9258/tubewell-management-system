from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from .forms import CustomLoginForm


urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', LoginView.as_view(
        template_name='accounts/login.html',
        authentication_form=CustomLoginForm
    ), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('renter-dashboard/', views.renter_dashboard, name='renter_dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]