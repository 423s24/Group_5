from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

ACCOUNT_TYPES = [
    ('admin', 'admin'),
    ('manager', 'manager'),
    ('teneant', 'tenant')
]

# Create your models here.

class UserAccount(AbstractUser): 
    # AbstractUser has fields: id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined
    twoFactorKey = models.CharField(max_length=100)
    manager = models.OneToOneField('Manager', on_delete=models.SET_NULL, null=True, blank=True)
    tenant = models.OneToOneField('Tenant', on_delete=models.SET_NULL, null=True, blank=True)
    #userHousingApplications = models.ManyToManyField('HousingApplication', through='UserHousingApplication')
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
            self.save()

class Tenant(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    unitId = models.IntegerField()
    dob = models.DateField()
    impairments = models.CharField(max_length=100)
    archived = models.BooleanField(default=False)

class Manager(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
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
    #units = models.ManyToManyField('Unit')

class Unit(models.Model):
    buildingId = models.ForeignKey('Building', on_delete=models.CASCADE)
    unitNumber = models.CharField(max_length=100)
    unitFloor = models.CharField(max_length=100, default='')
    unitSize = models.CharField(max_length=100, default='')
    unitName = models.CharField(max_length=100, default='')
    unitBedrooms = models.CharField(max_length=100, default='')

class MaintenanceRequest(models.Model):
    unitId = models.ForeignKey('Unit', null=True, on_delete=models.CASCADE) # Take out null=True when Unit is working
    building = models.ForeignKey('Building', null=True, on_delete=models.SET_NULL)
    userId = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
    entry_permission = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    title = models.CharField(max_length=100, default='')
    status = models.CharField(max_length=100, default='Open')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # address seems arbitrary kept it in but don't think its necessary
    address = models.CharField(max_length=100)
    unit = models.CharField(max_length=100, default='')
    request = models.CharField(max_length=10000)
    phone = models.CharField(max_length=100)
    dateCompleted = models.DateTimeField(null=True, blank=True)

class MaintenanceNotes(models.Model):
    maintenanceRequestId = models.ForeignKey('MaintenanceRequest', on_delete=models.CASCADE, related_name='maintenance_notes')
    userId = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
    dateMade = models.DateTimeField(null=True, blank=True)
    notes = models.CharField(max_length=10000, default='')
    tenantViewable = models.BooleanField(default=False)

class HousingApplication(models.Model):
    userId = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    unit_wanted = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
