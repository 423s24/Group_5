# Generated by Django 5.0.2 on 2024-04-24 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portal', '0034_alter_maintenancerequest_priority_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='account_type',
            field=models.CharField(choices=[('admin', 'Admin'), ('manager', 'Manager'), ('tenant', 'Tenant')], default='tenant', max_length=20),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='building_sort',
            field=models.CharField(choices=[('building_name', 'Building Name'), ('-building_name', 'Building Name (Descending)'), ('address', 'Address'), ('-address', 'Address (Descending)'), ('city', 'City'), ('-city', 'City (Descending)'), ('state', 'State'), ('-state', 'State (Descending)'), ('country', 'Country'), ('-country', 'Country (Descending)'), ('zipcode', 'Zipcode'), ('-zipcode', 'Zipcode (Descending)')], default='id', max_length=20),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='request_sort',
            field=models.CharField(choices=[('id', 'ID'), ('-id', 'ID (Descending)'), ('last_name', 'Last Name'), ('-last_name', 'Last Name (Descending)'), ('title', 'Title'), ('-title', 'Title (Descending)'), ('status', 'Status'), ('-status', 'Status (Descending)'), ('priority', 'Priority'), ('-priority', 'Priority (Descending)'), ('building', 'Building'), ('-building', 'Building (Descending)'), ('unit', 'Unit'), ('-unit', 'Unit (Descending)')], default='id', max_length=20),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='user_sort',
            field=models.CharField(choices=[('username', 'Username'), ('-username', 'Username (Descending)'), ('email', 'Email'), ('-email', 'Email (Descending)'), ('name', 'Name'), ('-name', 'Name (Descending)'), ('account_type', 'Account Type'), ('-account_type', 'Account Type (Descending)'), ('date_joined', 'Date Joined'), ('-date_joined', 'Date Joined (Descending)')], default='id', max_length=20),
        ),
    ]
