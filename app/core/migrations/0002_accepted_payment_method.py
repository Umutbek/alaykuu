# Generated by Django 4.0.3 on 2022-09-21 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accepted',
            name='payment_method',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Метод оплаты'),
        ),
    ]