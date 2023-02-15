from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('farmer', '0003_farmer_farmer_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmer',
            name='farmer_type',
            field=django_fsm.FSMIntegerField(blank=True, choices=[(1, 'Мелкий'), (2, 'Средний'), (3, 'Крупный')], null=True, verbose_name='Категории фермеров'),
        ),
    ]
