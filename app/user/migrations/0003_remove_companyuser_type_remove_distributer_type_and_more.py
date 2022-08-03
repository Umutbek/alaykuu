# Generated by Django 4.0.3 on 2022-08-03 05:57

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_companyuser_type_distributer_type_farmer_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyuser',
            name='type',
        ),
        migrations.RemoveField(
            model_name='distributer',
            name='type',
        ),
        migrations.RemoveField(
            model_name='farmer',
            name='type',
        ),
        migrations.AddField(
            model_name='user',
            name='type',
            field=django_fsm.FSMIntegerField(blank=True, choices=[(1, 'Пользователь Компании'), (2, 'Фермер'), (3, 'Поставшик')], null=True),
        ),
    ]
