# Generated by Django 5.0.2 on 2024-02-20 23:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenancerequest',
            name='unitId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Portal.unit'),
        ),
    ]
