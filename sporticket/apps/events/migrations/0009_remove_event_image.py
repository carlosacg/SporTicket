# Generated by Django 2.1.2 on 2018-11-06 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_event_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='image',
        ),
    ]