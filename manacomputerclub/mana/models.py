from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=255)
    # slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None,
                              blank=True, null=True, verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    
    def __str__(self):  # Это чтобы в консоли отображалось название, а не objects
        return self.title

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

        verbose_name = 'Новости'
        verbose_name_plural = "Новости"


class Computers(models.Model):
    STATUS_CHOICES = [
        ('default', 'Обычный зал'),
        ('vip', 'Вип зал'),
        ('premium', 'Премиум зал'),
    ]

    STATUS_WORK = [
        ('works', 'Работает'),
        ('broken', 'Сломан'),
    ]

    title = models.CharField(max_length=255)
    parameters = models.TextField(blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_WORK,
        default='works',
    )

    room = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='default',
    )

    def __str__(self):  # Это чтобы в консоли отображалось название, а не objects
        return self.title
    
    class Meta:
        verbose_name = 'Компьютер'
        verbose_name_plural = "Компьютеры"


class Services(models.Model):
    DURATION_CHOICES = [
        ('60', '1 час'),
        ('120', '2 часа'),
        ('180', '3 часа'),
        ('300', '5 часов'),
        ('480', '8 часов'),
        ('600', '10 часов'),
        ('720', '12 часов'),
        ('1440', '24 часа'),
    ]

    ROOM_CHOICES = [
        ('default', 'Обычный зал'),
        ('vip', 'Вип зал'),
        ('premium', 'Премиум зал'),
    ]

    title = models.CharField(max_length=255)
    room = models.CharField(
        max_length=20,
        choices=ROOM_CHOICES,
        default='default',
    )
    duration = models.CharField(
        max_length=20,
        choices=DURATION_CHOICES,
        default='60',
    )
    sum = models.IntegerField()

    def __str__(self):  # Это чтобы в консоли отображалось название, а не objects
        return self.title
    
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = "Услуги"