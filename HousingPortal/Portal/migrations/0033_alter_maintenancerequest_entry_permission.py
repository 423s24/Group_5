# Generated by Django 5.0.2 on 2024-04-22 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portal', '0032_useraccount_building_sort_useraccount_paging_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenancerequest',
            name='entry_permission',
            field=models.CharField(default='N/A', max_length=10),
        ),
    ]
