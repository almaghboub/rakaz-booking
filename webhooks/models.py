from django.db import models
from appointments.models import Appointment


class MessageLog(models.Model):
    DIRECTION_INBOUND = 'INBOUND'
    DIRECTION_OUTBOUND = 'OUTBOUND'

    DIRECTION_CHOICES = [
        (DIRECTION_INBOUND, 'Inbound'),
        (DIRECTION_OUTBOUND, 'Outbound'),
    ]

    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='message_logs')
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.direction} - {self.appointment} - {self.timestamp}"

    class Meta:
        verbose_name = 'Message Log'
        verbose_name_plural = 'Message Logs'
        ordering = ['-timestamp']
