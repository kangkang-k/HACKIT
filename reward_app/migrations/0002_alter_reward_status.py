# Generated by Django 5.2.1 on 2025-05-29 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reward_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reward',
            name='status',
            field=models.CharField(choices=[('accepted', 'Accepted'), ('waiting', 'Waiting'), ('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
    ]
