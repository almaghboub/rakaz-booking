from django.contrib import admin
from .models import Appointment


def confirm_appointments(modeladmin, request, queryset):
    queryset.update(status=Appointment.STATUS_CONFIRMED)
confirm_appointments.short_description = 'Confirm selected appointments'


def cancel_appointments(modeladmin, request, queryset):
    queryset.update(status=Appointment.STATUS_CANCELLED)
cancel_appointments.short_description = 'Cancel selected appointments'


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'phone', 'doctor', 'service', 'date', 'time', 'status', 'created_at')
    list_filter = ('status', 'doctor', 'date')
    search_fields = ('patient_name', 'phone')
    actions = [confirm_appointments, cancel_appointments]
    date_hierarchy = 'date'
