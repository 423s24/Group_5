# Generated by Django 5.0.2 on 2024-04-03 15:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Portal", "0022_rename_buildingname_building_building_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="maintenancerequest",
            name="priority",
            field=models.CharField(default="Low", max_length=100),
        ),
    ]
