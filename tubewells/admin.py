from django.contrib import admin
from .models import Tubewell, AuthorizedRenter


@admin.register(Tubewell)
class TubewellAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'location', 'rate_per_hour', 'created_at']
    list_filter = ['owner']


@admin.register(AuthorizedRenter)
class AuthorizedRenterAdmin(admin.ModelAdmin):
    list_display = ['renter', 'owner', 'tubewell', 'added_at']