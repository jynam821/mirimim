# Generated by Django 3.0.8 on 2020-07-20 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_classroom_sbj_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Refer',
            fields=[
                ('email', models.CharField(max_length=50)),
                ('refer_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
