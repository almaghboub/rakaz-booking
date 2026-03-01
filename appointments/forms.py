from django import forms
from .models import Appointment
from doctors.models import Doctor
from services.models import Service


class BookingForm(forms.Form):
    patient_name = forms.CharField(max_length=255, label='Patient Name')
    phone = forms.CharField(max_length=50, label='Phone Number')
    preferred_language = forms.ChoiceField(
        choices=Appointment.LANGUAGE_CHOICES,
        initial='ar',
        label='Preferred Language'
    )
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), label='Doctor')
    service = forms.ModelChoiceField(queryset=Service.objects.all(), label='Service')
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Date')
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label='Time')
