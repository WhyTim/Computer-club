from django.contrib import admin
from .models import Computers, News, Services

admin.site.register(News)
admin.site.register(Computers)
admin.site.register(Services)
