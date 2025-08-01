# Generated by Django 5.2.4 on 2025-07-17 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0002_room_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=20, unique=True)),
                ('from_city', models.CharField(max_length=100)),
                ('to_city', models.CharField(max_length=100)),
                ('departure', models.DateTimeField()),
                ('arrival', models.DateTimeField()),
            ],
        ),
    ]
