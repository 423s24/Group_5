# Generated by Django 5.0.2 on 2024-03-06 17:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Portal", "0014_alter_maintenancenotes_maintenancerequestid"),
    ]

    operations = [
        migrations.AddField(
            model_name="maintenancenotes",
            name="tenantViewable",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="maintenancerequest",
            name="status",
            field=models.CharField(default="Open", max_length=100),
        ),
        migrations.AddField(
            model_name="maintenancerequest",
            name="title",
            field=models.CharField(default="", max_length=100),
        ),
    ]
