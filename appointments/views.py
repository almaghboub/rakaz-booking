import json
from datetime import datetime, timedelta, time as time_type
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from .models import Appointment
from .forms import BookingForm
from doctors.models import Doctor
from services.models import Service
from webhooks.messages import CONFIRMATION_MESSAGE
from webhooks.models import MessageLog


DAY_MAP = {
    0: 'mon',
    1: 'tue',
    2: 'wed',
    3: 'thu',
    4: 'fri',
    5: 'sat',
    6: 'sun',
}


def generate_slots(doctor, service, date):
    """Generate available time slots for a doctor/service/date."""
    day_key = DAY_MAP.get(date.weekday())
    working = doctor.working_hours.get(day_key)
    if not working:
        return []

    try:
        start_str = working.get('start', '')
        end_str = working.get('end', '')
        if not start_str or not end_str:
            return []
        start_dt = datetime.strptime(start_str, '%H:%M')
        end_dt = datetime.strptime(end_str, '%H:%M')
    except (ValueError, AttributeError):
        return []

    slot_duration = service.duration_minutes + service.buffer_minutes
    if slot_duration <= 0:
        return []

    break_times = doctor.break_times or []

    booked_times = set(
        Appointment.objects.filter(
            doctor=doctor,
            date=date,
        ).exclude(status=Appointment.STATUS_CANCELLED).values_list('time', flat=True)
    )

    slots = []
    current = start_dt
    while current + timedelta(minutes=slot_duration) <= end_dt:
        slot_time = current.time()

        # Check if slot overlaps with any break
        in_break = False
        for br in break_times:
            try:
                br_start = datetime.strptime(br['start'], '%H:%M').time()
                br_end = datetime.strptime(br['end'], '%H:%M').time()
                slot_end_time = (current + timedelta(minutes=slot_duration)).time()
                if slot_time < br_end and slot_end_time > br_start:
                    in_break = True
                    break
            except (KeyError, ValueError):
                continue

        if not in_break and slot_time not in booked_times:
            slots.append(slot_time.strftime('%H:%M'))

        current += timedelta(minutes=slot_duration)

    return slots


def book_appointment(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            appointment = Appointment.objects.create(
                patient_name=data['patient_name'],
                phone=data['phone'],
                preferred_language=data['preferred_language'],
                doctor=data['doctor'],
                service=data['service'],
                date=data['date'],
                time=data['time'],
                status=Appointment.STATUS_PENDING,
            )

            # Simulate sending WhatsApp confirmation message
            lang = appointment.preferred_language
            msg = CONFIRMATION_MESSAGE[lang].format(
                name=appointment.patient_name,
                doctor=appointment.doctor.name,
                date=appointment.date.strftime('%Y-%m-%d'),
                time=appointment.time.strftime('%H:%M'),
            )
            # Log outbound message
            MessageLog.objects.create(
                appointment=appointment,
                direction='OUTBOUND',
                message=msg,
            )

            return redirect('appointments:confirmation', pk=appointment.pk)
    else:
        form = BookingForm()

    return render(request, 'appointments/book.html', {'form': form})


def confirmation(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'appointments/confirmation.html', {'appointment': appointment})


def available_slots(request):
    doctor_id = request.GET.get('doctor_id')
    service_id = request.GET.get('service_id')
    date_str = request.GET.get('date')

    if not all([doctor_id, service_id, date_str]):
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    try:
        doctor = Doctor.objects.get(pk=doctor_id)
        service = Service.objects.get(pk=service_id)
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except (Doctor.DoesNotExist, Service.DoesNotExist, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=400)

    slots = generate_slots(doctor, service, date)
    return JsonResponse({'slots': slots})
