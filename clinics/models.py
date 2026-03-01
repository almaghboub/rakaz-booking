from django.db import models


class Clinic(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=50)
    whatsapp_number = models.CharField(max_length=50)
    business_hours = models.JSONField(default=dict, help_text='e.g. {"mon": "08:00-17:00"}')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Clinic'
        verbose_name_plural = 'Clinics'
