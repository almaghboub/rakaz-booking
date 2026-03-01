from django.db import models
from django.contrib.auth.models import User
from clinics.models import Clinic


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctor_profile')
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    working_hours = models.JSONField(
        default=dict,
        help_text='e.g. {"mon": {"start": "08:00", "end": "17:00"}}'
    )
    break_times = models.JSONField(
        default=list,
        help_text='e.g. [{"start": "12:00", "end": "13:00"}]'
    )
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='doctors')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
