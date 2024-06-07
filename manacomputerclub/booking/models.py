from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from mana.models import Computers, Services

ADRESS_CHOICES = (
    ("Мостовицкая 7", "Мостовицкая 7"),
    ("Ленина 101А", "Ленина 101А"),
    ("Риммы Юровской 2А", "Риммы Юровской 2А"),
    )

TIME_CHOICES = (
    ("3:00", "3:00"),
    ("3:30 PM", "3:30 PM"),
    ("4 PM", "4 PM"),
    ("4:30 PM", "4:30 PM"),
    ("5 PM", "5 PM"),
    ("5:30 PM", "5:30 PM"),
    ("6 PM", "6 PM"),
    ("6:30 PM", "6:30 PM"),
    ("7 PM", "7 PM"),
    ("7:30 PM", "7:30 PM"),
)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    club = models.CharField(max_length=50, choices=ADRESS_CHOICES, default="Мостовицкая 7", verbose_name="Адрес клуба")
    day = models.DateField(default=datetime.now, verbose_name="Дата посещения")
    time = models.TimeField(verbose_name="Время посещения")
    duration = models.CharField(max_length=20,default='60', verbose_name="Длительность посещения")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Дата и время заказа")
    computers = models.ManyToManyField(Computers, blank=True)
    services = models.CharField(max_length=50, default="Обычный зал 1ч.", verbose_name="Услуга")
    count_services = models.CharField(max_length=20,default='1')
    num_computers = models.PositiveIntegerField(default=1, verbose_name="Количество компьютеров")
    total_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Сумма заказа")

    def __str__(self):
        return f"day: {self.day} | time: {self.time}"
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Заказы"
