from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'clinic', 'created_at')
    list_filter = ('clinic', 'specialty')
    search_fields = ('name', 'specialty')
    raw_id_fields = ('user',)
