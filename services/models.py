from django.db import models
from clinics.models import Clinic


class Service(models.Model):
    name = models.CharField(max_length=255)
    duration_minutes = models.IntegerField()
    buffer_minutes = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='services')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
