from django.contrib import admin
from .models import MessageLog


@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'direction', 'timestamp')
    list_filter = ('direction', 'timestamp')
    search_fields = ('message', 'appointment__patient_name', 'appointment__phone')
    readonly_fields = ('timestamp',)
