# Generated manually to update MedicineRequest model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicinerequest',
            name='medicine',
        ),
        migrations.AddField(
            model_name='medicinerequest',
            name='patient_name',
            field=models.CharField(max_length=150, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medicinerequest',
            name='contact_number',
            field=models.CharField(max_length=20, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medicinerequest',
            name='patient_age',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicinerequest',
            name='medicine_name',
            field=models.CharField(max_length=200, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medicinerequest',
            name='dosage',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medicinerequest',
            name='form_type',
            field=models.CharField(blank=True, choices=[('tablets', 'Tablets'), ('capsules', 'Capsules'), ('liquid', 'Liquid/Syrup'), ('injection', 'Injection'), ('cream', 'Cream/Ointment'), ('drops', 'Drops')], max_length=20),
        ),
        migrations.AddField(
            model_name='medicinerequest',
            name='urgency',
            field=models.CharField(choices=[('routine', 'Routine (3-5 days)'), ('urgent', 'Urgent (1-2 days)'), ('emergency', 'Emergency (Same day)')], default='routine', max_length=20),
        ),
        migrations.AddField(
            model_name='medicinerequest',
            name='doctor_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='medicinerequest',
            name='medical_condition',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medicinerequest',
            name='allergies',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='medicinerequest',
            name='additional_notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='medicinerequest',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='medicinerequest',
            name='admin_notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='medicinerequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('denied', 'Denied'), ('completed', 'Completed')], default='pending', max_length=20),
        ),
        migrations.AlterModelOptions(
            name='medicinerequest',
            options={'ordering': ['-requested_at']},
        ),
    ] 