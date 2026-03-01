from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('webhooks/', include('webhooks.urls')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('appointments/', include('appointments.urls')),
    path('dashboard/', include('dashboard.urls')),
    prefix_default_language=False,
)
