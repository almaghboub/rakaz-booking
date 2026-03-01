from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_redirect, name='home'),
    path('schedule/', views.schedule, name='schedule'),
    path('schedule/weekly/', views.weekly_schedule, name='weekly'),
    path('doctor-arrived/', views.doctor_arrived, name='doctor_arrived'),
    path('broadcast/', views.broadcast, name='broadcast'),
]
