# Generated by Django 5.2.4 on 2025-07-21 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0002_remove_doctor_user_doctor_available_days_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='available_days',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
