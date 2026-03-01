from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('book/', views.book_appointment, name='book'),
    path('book/confirmation/<int:pk>/', views.confirmation, name='confirmation'),
    path('slots/', views.available_slots, name='slots'),
]
