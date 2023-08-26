# Generated by Django 4.0.3 on 2023-08-23 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_accepted_ref_item_onec_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='accepted',
            name='farmerComment',
            field=models.TextField(blank=True, verbose_name='Комментарий фермера'),
        ),
        migrations.AddField(
            model_name='accepted',
            name='farmerReview',
            field=models.FloatField(default=0, verbose_name='Обзор фермера'),
        ),
    ]