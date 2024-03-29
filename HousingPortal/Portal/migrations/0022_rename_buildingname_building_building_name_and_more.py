# Generated by Django 5.0.2 on 2024-03-25 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portal', '0021_maintenancerequest_assigned_manager_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='building',
            old_name='buildingName',
            new_name='building_name',
        ),
        migrations.RenameField(
            model_name='maintenancenotes',
            old_name='dateMade',
            new_name='date_submitted',
        ),
        migrations.RenameField(
            model_name='maintenancenotes',
            old_name='tenantViewable',
            new_name='tenant_viewable',
        ),
        migrations.RenameField(
            model_name='maintenancenotes',
            old_name='userId',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='maintenancerequest',
            old_name='dateCompleted',
            new_name='date_completed',
        ),
        migrations.RenameField(
            model_name='maintenancerequest',
            old_name='userId',
            new_name='user_id',
        ),
        migrations.AddField(
            model_name='useraccount',
            name='email_notifications',
            field=models.BooleanField(default=False),
        ),
    ]
