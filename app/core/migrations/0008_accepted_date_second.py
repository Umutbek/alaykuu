# Generated by Django 4.0.3 on 2023-08-26 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_accepted_farmercomment_accepted_farmerreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='accepted',
            name='date_second',
            field=models.DateField(blank=True, null=True, verbose_name='Дата срока'),
        ),
    ]
