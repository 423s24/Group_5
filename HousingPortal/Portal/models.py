from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError

ACCOUNT_TYPES = [
    ('admin', 'Admin'),
    ('manager', 'Manager'),
    ('tenant', 'Tenant'),
]

STATUS = [
    ('New', 'New'),
    ('In Progress', 'In Progress'),
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
]

PRIORITY = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
    ('Urgent', 'Urgent'),
]

REQUEST_SORT = [
    ('id', 'ID'),
    ('-id', 'ID (Descending)'),
    ('last_name', 'Last Name'),
    ('-last_name', 'Last Name (Descending)'),
    ('title', 'Title'),
    ('-title', 'Title (Descending)'),
    ('status', 'Status'),
    ('-status', 'Status (Descending)'),
    ('priority', 'Priority'),
    ('-priority', 'Priority (Descending)'),
    ('building', 'Building'),
    ('-building', 'Building (Descending)'),
    ('unit', 'Unit'),
    ('-unit', 'Unit (Descending)'),
]

BUILDING_SORT = [
    ('building_name', 'Building Name'),
    ('-building_name', 'Building Name (Descending)'),
    ('address', 'Address'),
    ('-address', 'Address (Descending)'),
    ('city', 'City'),
    ('-city', 'City (Descending)'),
    ('state', 'State'),
    ('-state', 'State (Descending)'),
    ('country', 'Country'),
    ('-country', 'Country (Descending)'),
    ('zipcode', 'Zipcode'),
    ('-zipcode', 'Zipcode (Descending)'),
]

USER_SORT = [
    ('username', 'Username'),
    ('-username', 'Username (Descending)'),
    ('email', 'Email'),
    ('-email', 'Email (Descending)'),
    ('name', 'Name'),
    ('-name', 'Name (Descending)'),
    ('account_type', 'Account Type'),
    ('-account_type', 'Account Type (Descending)'),
    ('date_joined', 'Date Joined'),
    ('-date_joined', 'Date Joined (Descending)'),
]

PAGING_COUNT = [
    (10, '10 items per page'),
    (25, '25 items per page'),
    (50, '50 items per page'),
    (100, '100 items per page'),
]

class UsernameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(UsernameField, self).__init__(*args, **kwargs)
        # Add a validator to ensure the value contains only the specified characters
        self.validators.append(RegexValidator(r'^[a-z0-9\-_.]*$', 'Only lowercase letters, numbers, hyphen, underscore, and period are allowed.'))
        self.validators.append(MaxLengthValidator(30, message='Username must be at most 30 characters long.'))
        self.validators.append(MinLengthValidator(1, message='Username must be at least 1 character long.'))

# Create your models here.

class UserAccount(AbstractUser): 
    # AbstractUser has fields: id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined
    username = UsernameField(unique=True)
    is_manager = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    email_notifications = models.BooleanField(default=False)
    request_sort = models.CharField(max_length=20, choices=REQUEST_SORT, default='id')
    building_sort = models.CharField(max_length=20, choices=BUILDING_SORT, default='building_name')
    user_sort = models.CharField(max_length=20, choices=USER_SORT, default='date_joined')
    paging_count = models.PositiveSmallIntegerField(choices=PAGING_COUNT, default=25)

    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='tenant')

    # Override the save method to synchronize account_type with is_superuser and is_manager
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.account_type = 'admin'
        elif self.is_manager:
            self.account_type = 'manager'
        else:
            self.account_type = 'tenant'
        super().save(*args, **kwargs)

    # @property
    # def account_type(self):
    #     if (self.is_superuser):
    #         return 'admin'
    #     elif (self.is_manager):
    #         return 'manager'
    #     else:
    #         return 'tenant'
        
    def setAccountType(self, account_type):
        if account_type not in dict(ACCOUNT_TYPES):
            raise ValueError
        if self.account_type == account_type:
            return
        
        if account_type == 'admin':
            self.is_manager = False
            self.is_superuser = True
            self.save()
        elif account_type == 'manager':
            self.is_manager = True
            self.is_superuser = False
            self.save()
        elif account_type == 'tenant':
            self.is_manager = False
            self.is_superuser = False
            self.save()

class UserAccountMaintenanceRequest(models.Model):
    user_id = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
    maintenanceRequest_id = models.ForeignKey('MaintenanceRequest', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_id', 'maintenanceRequest_id')

class Building(models.Model):
    building_name = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)

class MaintenanceRequest(models.Model):
    user_id = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
    assigned_manager = models.ForeignKey('UserAccount', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_manager')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    unit = models.CharField(max_length=100, default='')
    building = models.ForeignKey('Building', null=True, on_delete=models.SET_NULL)
    date_submitted = models.DateTimeField(null=True, blank=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS, default='New')
    priority = models.CharField(max_length=100, choices=PRIORITY, default='Low')
    title = models.CharField(max_length=100, default='')
    request = models.CharField(max_length=10000)
    entry_permission = models.CharField(max_length=10, default='N/A')

class MaintenanceNotes(models.Model):
    maintenanceRequestId = models.ForeignKey('MaintenanceRequest', on_delete=models.CASCADE, related_name='maintenance_notes')
    user_id = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
    date_submitted = models.DateTimeField(null=True, blank=True)
    tenant_viewable = models.BooleanField(default=False)
    notes = models.CharField(max_length=10000, default='')

def maintenance_file_path(instance, filename):
    return f'maintenance_files/{instance.maintenanceRequestId.id}/{filename}'

class MaintenanceFile(models.Model):
    maintenanceRequestId = models.ForeignKey('MaintenanceRequest', on_delete=models.CASCADE, related_name='maintenance_files')
    file = models.FileField(upload_to=maintenance_file_path)
