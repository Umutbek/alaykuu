# Generated by Django 4.0.3 on 2023-06-20 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmer', '0008_remove_cartitems_order_farmerorders_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmer',
            name='oneC_id',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='1С ID'),
        ),
    ]
