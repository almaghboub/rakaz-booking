from django.contrib import admin
from .models import Clinic


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'whatsapp_number', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'address', 'phone')
