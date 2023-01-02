# Generated by Django 4.1.4 on 2022-12-30 06:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_city_options_alter_district_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LaborantUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Лаборант',
                'verbose_name_plural': 'Лаборанты',
            },
            bases=('user.user',),
        ),
        migrations.AlterField(
            model_name='user',
            name='type',
            field=django_fsm.FSMIntegerField(blank=True, choices=[(1, 'Пользователь Компании'), (2, 'Фермер'), (3, 'Поставшик'), (4, 'ЛАБОРАНТ')], null=True),
        ),
    ]
