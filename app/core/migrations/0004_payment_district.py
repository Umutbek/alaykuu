# Generated by Django 4.0.3 on 2023-03-27 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_model1cuser_alter_user_type'),
        ('core', '0003_payment_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.district', verbose_name='Район'),
        ),
    ]
