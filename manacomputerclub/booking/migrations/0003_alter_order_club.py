# Generated by Django 4.2.1 on 2024-06-01 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_alter_order_club'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='club',
            field=models.CharField(choices=[('Мостовицкая 7', 'Мостовицкая 7'), ('Ленина 101А', 'Ленина 101А'), ('Риммы Юровской 2А', 'Риммы Юровской 2А')], default='Мостовицкая 7', max_length=50),
        ),
    ]
