# Generated by Django 5.0.2 on 2024-03-04 00:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Portal", "0006_maintenancerequest_building"),
    ]

    operations = [
        migrations.AddField(
            model_name="maintenancerequest",
            name="entry_permission",
            field=models.BooleanField(default=False),
        ),
    ]