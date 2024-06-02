# Тут описываются различные маршруты
from django.conf.urls.static import static
from manacomputerclub import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mana.urls')),
    path('users/', include('users.urls', namespace="users")),
    path("booking/", include("booking.urls", namespace="booking")),
]

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Администрирование сайта Mana"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)