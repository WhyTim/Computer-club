from django.db import models


# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    # slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(blank=True, verbose_name="Содержание")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None,
                              blank=True, null=True, verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовать?")

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

    title = models.CharField(max_length=255, verbose_name="Название")
    parameters = models.TextField(blank=True, verbose_name="Комментарий")
    status = models.CharField(
        max_length=10,
        choices=STATUS_WORK,
        default='works',
        verbose_name="Статус"
    )

    room = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='default',
        verbose_name="Комната"
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

    title = models.CharField(max_length=255, verbose_name="Название")
    room = models.CharField(
        max_length=20,
        choices=ROOM_CHOICES,
        default='default', 
        verbose_name="Комната"

    )
    duration = models.CharField(
        max_length=20,
        choices=DURATION_CHOICES,
        default='60',
        verbose_name="Длительность"
    )
    sum = models.IntegerField(verbose_name="Сумма")

    def __str__(self):  # Это чтобы в консоли отображалось название, а не objects
        return self.title

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = "Услуги"
