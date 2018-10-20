# Generated by Django 2.1.2 on 2018-10-19 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('initial_date', models.DateField()),
                ('initial_time', models.TimeField()),
                ('place', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=20)),
                ('capacity', models.IntegerField()),
                ('visitor', models.CharField(max_length=200)),
                ('local', models.CharField(max_length=200)),
                ('event_type', models.CharField(max_length=200)),
            ],
        ),
    ]