# Generated by Django 5.2.4 on 2025-07-17 08:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0005_payment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, '1 - Very Poor'), (2, '2 - Poor'), (3, '3 - Average'), (4, '4 - Good'), (5, '5 - Excellent')])),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_feedbacks', to='hotel.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_feedbacks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
