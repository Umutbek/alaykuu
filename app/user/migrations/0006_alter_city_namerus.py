# Generated by Django 4.0.3 on 2023-02-21 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_user_passport_back_alter_user_passport_front'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='nameRus',
            field=models.CharField(max_length=200, verbose_name='Название на русском'),
        ),
    ]
