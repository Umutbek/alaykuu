# Generated by Django 4.0.3 on 2022-08-03 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_salefarmercategory_webproducts_video_thumbnail_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='accepted',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата'),
        ),
    ]
