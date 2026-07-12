from django.urls import path
from . import views

urlpatterns = [
    path('record/<int:tubewell_id>/renter/<int:renter_id>/', views.record_payment, name='record_payment'),
]