# Generated by Django 2.1.3 on 2019-03-11 19:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='date_bill',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
