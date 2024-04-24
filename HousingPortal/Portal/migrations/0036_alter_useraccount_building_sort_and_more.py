# Generated by Django 5.0.2 on 2024-04-24 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portal', '0035_useraccount_account_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='building_sort',
            field=models.CharField(choices=[('building_name', 'Building Name'), ('-building_name', 'Building Name (Descending)'), ('address', 'Address'), ('-address', 'Address (Descending)'), ('city', 'City'), ('-city', 'City (Descending)'), ('state', 'State'), ('-state', 'State (Descending)'), ('country', 'Country'), ('-country', 'Country (Descending)'), ('zipcode', 'Zipcode'), ('-zipcode', 'Zipcode (Descending)')], default='building_name', max_length=20),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='user_sort',
            field=models.CharField(choices=[('username', 'Username'), ('-username', 'Username (Descending)'), ('email', 'Email'), ('-email', 'Email (Descending)'), ('name', 'Name'), ('-name', 'Name (Descending)'), ('account_type', 'Account Type'), ('-account_type', 'Account Type (Descending)'), ('date_joined', 'Date Joined'), ('-date_joined', 'Date Joined (Descending)')], default='date_joined', max_length=20),
        ),
    ]
