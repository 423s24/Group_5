# Generated by Django 5.0.2 on 2024-02-26 23:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Portal", "0002_alter_maintenancerequest_unitid"),
    ]

    operations = [
        migrations.AddField(
            model_name="building",
            name="buildingName",
            field=models.CharField(default="Building", max_length=100),
            preserve_default=False,
        ),
    ]
