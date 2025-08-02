# Generated manually to update Notification model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='prescription',
        ),
        migrations.AddField(
            model_name='notification',
            name='title',
            field=models.CharField(max_length=200, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('appointment', 'Appointment'), ('medicine', 'Medicine'), ('package', 'Package'), ('admin', 'Admin'), ('system', 'System')], default='system', max_length=20),
        ),
        migrations.AddField(
            model_name='notification',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notification',
            name='related_id',
            field=models.IntegerField(blank=True, help_text='ID of related object (appointment, medicine request, etc.)', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='admin_notes',
            field=models.TextField(blank=True, help_text='Internal notes for admin'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='is_sent',
            field=models.BooleanField(default=True, help_text='Default to True for immediate notifications'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='scheduled_time',
            field=models.DateTimeField(blank=True, help_text='Time when the notification should be triggered (for scheduled notifications).', null=True),
        ),
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddIndex(
            model_name='notification',
            index=models.Index(fields=['patient', 'is_read'], name='notification_patient_2b8c8c_idx'),
        ),
        migrations.AddIndex(
            model_name='notification',
            index=models.Index(fields=['notification_type'], name='notification_notifica_8c8c8c_idx'),
        ),
        migrations.AddIndex(
            model_name='notification',
            index=models.Index(fields=['created_at'], name='notification_created_8c8c8c_idx'),
        ),
    ] 