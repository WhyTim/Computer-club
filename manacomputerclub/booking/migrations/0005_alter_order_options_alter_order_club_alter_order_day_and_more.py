# Generated by Django 4.2.1 on 2024-06-06 16:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_remove_order_time_intervals_order_count_services_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterField(
            model_name='order',
            name='club',
            field=models.CharField(choices=[('Мостовицкая 7', 'Мостовицкая 7'), ('Ленина 101А', 'Ленина 101А'), ('Риммы Юровской 2А', 'Риммы Юровской 2А')], default='Мостовицкая 7', max_length=50, verbose_name='Адрес клуба'),
        ),
        migrations.AlterField(
            model_name='order',
            name='day',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Дата посещения'),
        ),
        migrations.AlterField(
            model_name='order',
            name='duration',
            field=models.CharField(default='60', max_length=20, verbose_name='Длительность посещения'),
        ),
        migrations.AlterField(
            model_name='order',
            name='num_computers',
            field=models.PositiveIntegerField(default=1, verbose_name='Количество компьютеров'),
        ),
        migrations.RemoveField(
            model_name='order',
            name='services',
        ),
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.TimeField(verbose_name='Время посещения'),
        ),
        migrations.AlterField(
            model_name='order',
            name='time_ordered',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Дата и время заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_sum',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Сумма заказа'),
        ),
        migrations.AddField(
            model_name='order',
            name='services',
            field=models.CharField(default='Обычный зал 1ч.', max_length=50, verbose_name='Услуга'),
        ),
    ]
