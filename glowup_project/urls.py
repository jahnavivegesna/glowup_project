"""GLOW UP - Main URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Customize admin site
admin.site.site_header = "GLOW UP Admin"
admin.site.site_title = "GLOW UP Admin Portal"
admin.site.index_title = "Welcome to GLOW UP Admin"
