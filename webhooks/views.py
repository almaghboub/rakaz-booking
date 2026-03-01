import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings

from appointments.models import Appointment
from .models import MessageLog
from .messages import CONFIRMED_MESSAGE, CANCELLED_MESSAGE


@csrf_exempt
@require_http_methods(["POST"])
def whatsapp_webhook(request):
    token = request.headers.get('X-Webhook-Token', '')
    if token != settings.WHATSAPP_WEBHOOK_TOKEN:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    phone = data.get('phone', '').strip()
    message = data.get('message', '').strip().upper()

    if not phone or not message:
        return JsonResponse({'error': 'Missing phone or message'}, status=400)

    appointment = (
        Appointment.objects.filter(
            phone=phone,
            status=Appointment.STATUS_PENDING,
        )
        .order_by('-created_at')
        .first()
    )

    if not appointment:
        return JsonResponse({'error': 'No pending appointment found for this phone'}, status=404)
    lang = appointment.preferred_language

    # Log inbound message
    MessageLog.objects.create(
        appointment=appointment,
        direction=MessageLog.DIRECTION_INBOUND,
        message=data.get('message', ''),
    )

    if message in ('YES', 'نعم'):
        appointment.status = Appointment.STATUS_CONFIRMED
        appointment.save()
        reply = CONFIRMED_MESSAGE[lang]
    elif message in ('NO', 'لا'):
        appointment.status = Appointment.STATUS_CANCELLED
        appointment.save()
        reply = CANCELLED_MESSAGE[lang]
    else:
        return JsonResponse({'error': 'Unrecognized message. Send YES/NO or نعم/لا'}, status=400)

    # Log outbound reply
    MessageLog.objects.create(
        appointment=appointment,
        direction=MessageLog.DIRECTION_OUTBOUND,
        message=reply,
    )

    return JsonResponse({'status': appointment.status, 'reply': reply})
