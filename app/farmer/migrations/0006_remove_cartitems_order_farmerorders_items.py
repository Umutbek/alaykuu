# Generated by Django 4.0.3 on 2023-04-01 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmer', '0005_salefarmeritem_districts_salefarmeritem_is_sale_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitems',
            name='order',
        ),
        migrations.AddField(
            model_name='farmerorders',
            name='items',
            field=models.ManyToManyField(blank=True, to='farmer.cartitems', verbose_name='Товары'),
        ),
    ]