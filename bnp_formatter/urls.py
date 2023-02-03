from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from main.views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="homepage"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
