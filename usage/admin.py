from django.contrib import admin
from .models import UsageRecord


@admin.register(UsageRecord)
class UsageRecordAdmin(admin.ModelAdmin):
    list_display = ['tubewell', 'used_by', 'status', 'start_time', 'end_time', 'total_hours', 'amount']
    list_filter = ['status', 'tubewell']