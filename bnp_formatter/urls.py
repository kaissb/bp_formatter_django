from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from main.views import home, download_output

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="homepage"),
    path("do/<int:pk>", download_output, name="download_output"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
