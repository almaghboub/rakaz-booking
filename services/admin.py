from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_minutes', 'buffer_minutes', 'price', 'clinic', 'created_at')
    list_filter = ('clinic',)
    search_fields = ('name',)
