# Generated by Django 3.0.8 on 2020-07-19 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20200719_1153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='content',
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='title',
        ),
    ]
