# Generated by Django 4.0.3 on 2023-02-15 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_accepted_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='products',
            field=models.ManyToManyField(blank=True, null=True, to='core.accepted', verbose_name='Продукты'),
        ),
    ]
