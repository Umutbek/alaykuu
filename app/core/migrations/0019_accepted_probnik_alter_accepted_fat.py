# Generated by Django 4.0.3 on 2023-09-07 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='accepted',
            name='probnik',
            field=models.FloatField(default=0, verbose_name='Пробник'),
        ),
        migrations.AlterField(
            model_name='accepted',
            name='fat',
            field=models.FloatField(default=0, verbose_name='Общая жирность'),
        ),
    ]
