# Generated by Django 4.0.3 on 2023-02-21 05:23

import core.imggenerate
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_delete_laborantuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='passport_back',
            field=models.FileField(blank=True, null=True, upload_to=core.imggenerate.all_image_file_path, verbose_name='Паспорт оборотная сторона'),
        ),
        migrations.AlterField(
            model_name='user',
            name='passport_front',
            field=models.FileField(blank=True, null=True, upload_to=core.imggenerate.all_image_file_path, verbose_name='Паспорт лицовая сторона'),
        ),
    ]
