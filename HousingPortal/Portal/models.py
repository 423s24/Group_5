from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

ACCOUNT_TYPES = [
    ('admin', 'admin'),
    ('manager', 'manager'),
    ('tenant', 'tenant'),
]

STATUS = [
    ('new', 'new'),
    ('pending', 'pending'),
]

# Create your models here.

class UserAccount(AbstractUser): 
    # AbstractUser has fields: id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined
    manager = models.OneToOneField('Manager', on_delete=models.SET_NULL, null=True, blank=True)
    archived = models.BooleanField(default=False)

    @property
    def account_type(self):
        if (self.is_superuser):
            return 'admin'
        elif (self.manager != None):
            return 'manager'
        else:
            return 'tenant'
        
    def setAccountType(self, account_type):
        if account_type not in dict(ACCOUNT_TYPES):
            raise ValueError
        if self.account_type == account_type:
            return
        
        if account_type == 'admin':
            if self.manager != None:
                Manager.objects.get(pk=self.manager.id).delete()
                self.manager = None
            self.is_superuser = True
            self.save()
        elif account_type == 'manager':
            if self.is_superuser:
                self.is_superuser = False
            manager = Manager()
            manager.save()
            self.manager = manager
            self.save()
        elif account_type == 'tenant':
            if self.is_superuser:
                self.is_superuser = False
            elif self.manager != None:
                Manager.objects.get(pk=self.manager.id).delete()
                self.manager = None
            self.save()

class Manager(models.Model):
    archived = models.BooleanField(default=False)
    #managerBuilding = models.ManyToManyField('Building', through='ManagerBuilding')

class ManagerBuilding(models.Model):
    managerId = models.ForeignKey('Manager', on_delete=models.CASCADE)
    buildingId = models.ForeignKey('Building', on_delete=models.CASCADE)

class Building(models.Model):
    buildingName = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)

class MaintenanceRequest(models.Model):
    userId = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    unit = models.CharField(max_length=100, default='')
    building = models.ForeignKey('Building', null=True, on_delete=models.SET_NULL)
    # address seems arbitrary kept it in but don't think its necessary
    address = models.CharField(max_length=100)
    date_submitted = models.DateTimeField(null=True, blank=True)
    dateCompleted = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=100, default='New')
    title = models.CharField(max_length=100, default='')
    request = models.CharField(max_length=10000)
    entry_permission = models.BooleanField(default=False)

class MaintenanceNotes(models.Model):
    maintenanceRequestId = models.ForeignKey('MaintenanceRequest', on_delete=models.CASCADE, related_name='maintenance_notes')
    userId = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
    dateMade = models.DateTimeField(null=True, blank=True)
    tenantViewable = models.BooleanField(default=False)
    notes = models.CharField(max_length=10000, default='')
