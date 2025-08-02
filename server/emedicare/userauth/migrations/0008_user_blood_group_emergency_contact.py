# Generated manually to add blood_group and emergency_contact fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0007_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='blood_group',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='emergency_contact',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ] 