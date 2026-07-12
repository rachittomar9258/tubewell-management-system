from django.urls import path
from . import views

urlpatterns = [
    path('', views.owner_dashboard, name='owner_dashboard'),
    path('add/', views.add_tubewell, name='add_tubewell'),
    path('<int:tubewell_id>/', views.tubewell_detail, name='tubewell_detail'),
    path('<int:tubewell_id>/edit/', views.edit_tubewell, name='edit_tubewell'),
    path('<int:tubewell_id>/delete/', views.delete_tubewell, name='delete_tubewell'),
    path('<int:tubewell_id>/reactivate/', views.reactivate_tubewell, name='reactivate_tubewell'),
    path('<int:tubewell_id>/renter/<int:renter_id>/remove/', views.remove_renter, name='remove_renter'),
    path('<int:tubewell_id>/renter/<int:renter_id>/restore/', views.restore_renter, name='restore_renter'),
]
