# Generated by Django 4.2.1 on 2024-05-29 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mana', '0004_computers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('sum', models.IntegerField()),
                ('duration', models.CharField(choices=[(60, '1 час'), (120, '2 часа'), (180, '3 часа'), (300, '5 часов'), (480, '8 часов'), (600, '10 часов'), (720, '12 часов'), (1440, '24 часа')], default=60, max_length=20)),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
            },
        ),
    ]
