from django.urls import path
from . import views

urlpatterns = [
    path('', views.owner_dashboard, name='owner_dashboard'),
    path('add/', views.add_tubewell, name='add_tubewell'),
    path('<int:tubewell_id>/', views.tubewell_detail, name='tubewell_detail'),
    path('<int:tubewell_id>/edit/', views.edit_tubewell, name='edit_tubewell'),
]