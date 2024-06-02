# Generated by Django 4.2.1 on 2024-06-01 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_alter_order_club'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='time_intervals',
        ),
        migrations.AddField(
            model_name='order',
            name='count_services',
            field=models.CharField(default='1', max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='duration',
            field=models.CharField(default='60', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.TimeField(),
        ),
        migrations.DeleteModel(
            name='TimeInterval',
        ),
    ]
