# Generated by Django 4.2.1 on 2024-05-29 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mana', '0005_services'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='room',
            field=models.CharField(choices=[('default', 'Обычный зал'), ('vip', 'Вип зал'), ('premium', 'Премиум зал')], default='default', max_length=20),
        ),
        migrations.AlterField(
            model_name='services',
            name='duration',
            field=models.CharField(choices=[('60', '1 час'), ('120', '2 часа'), ('180', '3 часа'), ('300', '5 часов'), ('480', '8 часов'), ('600', '10 часов'), ('720', '12 часов'), ('1440', '24 часа')], default='60', max_length=20),
        ),
    ]
