from django.db import models
from django.conf import settings


class Tubewell(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tubewells',
        limit_choices_to={'role': 'owner'}
    )
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True, null=True)
    rate_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.owner.username}"

class AuthorizedRenter(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authorized_renters',
        limit_choices_to={'role': 'owner'}
    )
    renter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authorized_by_owners',
        limit_choices_to={'role': 'renter'}
    )
    tubewell = models.ForeignKey(
        Tubewell,
        on_delete=models.CASCADE,
        related_name='authorized_renters'
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('owner', 'renter', 'tubewell')

    def __str__(self):
        return f"{self.renter.username} authorized for {self.tubewell.name}"