from django.db import models
from django.conf import settings
from tubewells.models import Tubewell
from decimal import Decimal


class UsageRecord(models.Model):
    STATUS_CHOICES = (
        ('running', 'Running'),
        ('completed', 'Completed'),
    )

    tubewell = models.ForeignKey(Tubewell, on_delete=models.CASCADE, related_name='usage_records')
    used_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='usage_records'
    )
    is_self_use = models.BooleanField(default=False)

    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    rate_per_hour = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    total_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='running')
    sms_sent = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.rate_per_hour is None and self.tubewell_id:
            self.rate_per_hour = self.tubewell.rate_per_hour

        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            hours = Decimal(duration.total_seconds()) / Decimal(3600)
            self.total_hours = round(hours, 2)

            if self.rate_per_hour:
                self.amount = round(self.total_hours * self.rate_per_hour, 2)

            self.status = 'completed'

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.tubewell.name} - {self.used_by.username} ({self.status})"