# Generated by Django 4.0.3 on 2022-08-03 16:46

import core.imggenerate
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_fsm


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('fullname', models.CharField(max_length=200, verbose_name='Название')),
                ('login', models.CharField(max_length=200, unique=True, verbose_name='Логин')),
                ('phone', models.CharField(blank=True, max_length=200, null=True, verbose_name='Телефон номер')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=core.imggenerate.all_image_file_path, verbose_name='Фото')),
                ('passport_front', models.ImageField(blank=True, null=True, upload_to=core.imggenerate.all_image_file_path, verbose_name='Паспорт лицовая сторона')),
                ('passport_back', models.ImageField(blank=True, null=True, upload_to=core.imggenerate.all_image_file_path, verbose_name='Паспорт оборотная сторона')),
                ('passport_text', models.CharField(blank=True, max_length=200, null=True, verbose_name='Паспорт номер')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Адресс')),
                ('comment', models.CharField(blank=True, max_length=200, null=True, verbose_name='Комментарии')),
                ('active', models.BooleanField(default=False)),
                ('rating', models.FloatField(default=0, verbose_name='Рейтинг')),
                ('type', django_fsm.FSMIntegerField(blank=True, choices=[(1, 'Пользователь Компании'), (2, 'Фермер'), (3, 'Поставшик')], null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameEn', models.CharField(max_length=200, null=True, verbose_name='Название на английском')),
                ('nameRus', models.CharField(max_length=200, null=True, verbose_name='Название на русском')),
                ('nameKg', models.CharField(max_length=200, null=True, verbose_name='Название на кыргызком')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='CompanyUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('access_level', models.IntegerField(default=0, verbose_name='Доступ')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            bases=('user.user',),
        ),
        migrations.CreateModel(
            name='Distributer',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Распределитель',
                'verbose_name_plural': 'Распределители',
                'ordering': ('-id',),
            },
            bases=('user.user',),
        ),
        migrations.CreateModel(
            name='Farmer',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('payment_left', models.FloatField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Фермер',
                'verbose_name_plural': 'Фермеры',
                'ordering': ('-id',),
            },
            bases=('user.user',),
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameEn', models.CharField(max_length=200, null=True, verbose_name='Название на английском')),
                ('nameRus', models.CharField(max_length=200, null=True, verbose_name='Название на русском')),
                ('nameKg', models.CharField(max_length=200, null=True, verbose_name='Название на кыргызком')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.city', verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Область',
                'verbose_name_plural': 'Области',
                'ordering': ('id',),
            },
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='farmer_city', to='user.city', verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='user',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='farmer_district', to='user.district', verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
