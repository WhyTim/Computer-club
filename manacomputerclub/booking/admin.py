from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Order)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("time_ordered", "day", "time", "club", "total_sum", "num_computers")
    ordering = ("-time_ordered",)