# Тут описываются различные маршруты

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mana.urls')),
    path('users/', include('users.urls', namespace="users")),
    path("booking2/", include("booking.urls")),
]
