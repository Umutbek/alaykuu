# Generated by Django 4.0.3 on 2023-08-28 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_remove_accepted_date_other'),
    ]

    operations = [
        migrations.AddField(
            model_name='accepted',
            name='payment_type',
            field=models.CharField(choices=[('card', 'С картой'), ('cash', 'С наличными')], default='cash', max_length=10, verbose_name='Тип оплаты'),
        ),
    ]
