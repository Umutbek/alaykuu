# Generated by Django 4.0.3 on 2022-08-08 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_accepted_farmer_alter_payment_farmer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salefarmeritem',
            name='category',
        ),
        migrations.DeleteModel(
            name='SaleFarmerCategory',
        ),
        migrations.DeleteModel(
            name='SaleFarmerItem',
        ),
    ]
