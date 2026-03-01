# rakaz-booking
MVP Smart Clinic Booking System (Arabic + English)

## Codespaces Setup

```bash
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Features
- Smart clinic appointment booking
- Arabic (RTL) and English support
- WhatsApp webhook for appointment confirmation
- Doctor dashboard with daily/weekly schedule
- Admin panel for managing clinics, doctors, services, appointments
