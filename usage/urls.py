from django.urls import path
from . import views

urlpatterns = [
    path('<int:tubewell_id>/renter/<int:renter_id>/', views.renter_action_panel, name='renter_action_panel'),
    path('<int:tubewell_id>/renter/<int:renter_id>/start/', views.start_usage, name='start_usage'),
    path('<int:tubewell_id>/renter/<int:renter_id>/stop/', views.stop_usage, name='stop_usage'),
    path('history/<int:tubewell_id>/', views.my_usage_history, name='my_usage_history'),
]