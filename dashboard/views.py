from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from appointments.models import Appointment
from doctors.models import Doctor
from webhooks.models import MessageLog
from webhooks.messages import DOCTOR_ARRIVED_BROADCAST


@login_required
def dashboard_redirect(request):
    return redirect('dashboard:schedule')


@login_required
def schedule(request):
    today = date.today()
    doctor_id = request.GET.get('doctor_id')

    appointments = Appointment.objects.filter(date=today).select_related('doctor', 'service')
    doctors = Doctor.objects.all()

    if doctor_id:
        appointments = appointments.filter(doctor_id=doctor_id)

    # If the logged-in user is a doctor, restrict to their own schedule by default
    if not doctor_id and hasattr(request.user, 'doctor_profile'):
        appointments = appointments.filter(doctor=request.user.doctor_profile)

    context = {
        'appointments': appointments,
        'doctors': doctors,
        'selected_doctor_id': doctor_id,
        'today': today,
    }
    return render(request, 'dashboard/schedule.html', context)


@login_required
def weekly_schedule(request):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    doctor_id = request.GET.get('doctor_id')

    appointments = Appointment.objects.filter(
        date__gte=start_of_week,
        date__lte=end_of_week,
    ).select_related('doctor', 'service').order_by('date', 'time')

    doctors = Doctor.objects.all()

    if doctor_id:
        appointments = appointments.filter(doctor_id=doctor_id)

    context = {
        'appointments': appointments,
        'doctors': doctors,
        'selected_doctor_id': doctor_id,
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
    }
    return render(request, 'dashboard/weekly.html', context)


@login_required
@require_http_methods(["POST"])
def doctor_arrived(request):
    doctor_id = request.POST.get('doctor_id')
    today = date.today()

    try:
        doctor = Doctor.objects.get(pk=doctor_id)
    except Doctor.DoesNotExist:
        return JsonResponse({'error': 'Doctor not found'}, status=404)

    # Get today's confirmed appointments for the doctor
    confirmed_appointments = Appointment.objects.filter(
        doctor=doctor,
        date=today,
        status=Appointment.STATUS_CONFIRMED,
    )

    for appt in confirmed_appointments:
        msg = DOCTOR_ARRIVED_BROADCAST[appt.preferred_language].format(
            doctor=doctor.name,
            time=appt.time.strftime('%H:%M'),
        )
        MessageLog.objects.create(
            appointment=appt,
            direction=MessageLog.DIRECTION_OUTBOUND,
            message=f'[DOCTOR ARRIVED] {msg}',
        )

    return JsonResponse({'status': 'ok', 'notified': confirmed_appointments.count()})


@login_required
@require_http_methods(["POST"])
def broadcast(request):
    doctor_id = request.POST.get('doctor_id')
    broadcast_message = request.POST.get('message', '')
    today = date.today()

    confirmed_appointments = Appointment.objects.filter(
        date=today,
        status=Appointment.STATUS_CONFIRMED,
    )

    if doctor_id:
        confirmed_appointments = confirmed_appointments.filter(doctor_id=doctor_id)

    count = 0
    for appt in confirmed_appointments:
        MessageLog.objects.create(
            appointment=appt,
            direction=MessageLog.DIRECTION_OUTBOUND,
            message=broadcast_message or f'Broadcast to {appt.patient_name}',
        )
        count += 1

    return JsonResponse({'status': 'ok', 'sent': count})
