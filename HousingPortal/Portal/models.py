from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

# Create your models here.


class UserAccount(AbstractUser):
    username = models.CharField(max_length=50, editable=True, unique=True)
    email = models.EmailField(primary_key=True, unique=True)
    password = models.CharField(max_length=100)
    admin = models.BooleanField(default=False)
    twoFactorKey = models.CharField(max_length=100)
    manager = models.OneToOneField('Manager', on_delete=models.SET_NULL, null=True, blank=True)
    tenant = models.OneToOneField('Tenant', on_delete=models.SET_NULL, null=True, blank=True)
    userHousingApplications = models.ManyToManyField('HousingApplication', through='UserHousingApplication')
    maintenanceRequest = models.ForeignKey('MaintenanceRequest', on_delete=models.CASCADE, null=True)
    archived = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super(UserAccount, self).save(*args, **kwargs)


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
    managerBuilding = models.ManyToManyField('Building', through='ManagerBuilding')


class ManagerBuilding(models.Model):
    managerId = models.ForeignKey('Manager', on_delete=models.CASCADE)
    buildingId = models.ForeignKey('Building', on_delete=models.CASCADE)


class Building(models.Model):
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    units = models.ManyToManyField('Unit')


class Unit(models.Model):
    buildingId = models.ForeignKey('Building', on_delete=models.CASCADE)
    unitNumber = models.CharField(max_length=100)
    maintenanceRequests = models.ManyToManyField('MaintenanceRequest')


class MaintenanceRequest(models.Model):
    completed = models.BooleanField(default=False)


class UserHousingApplication(models.Model):
    userId = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
    housingApplicationId = models.ForeignKey('HousingApplication', on_delete=models.CASCADE)


class HousingApplication(models.Model):
    temporary = models.BooleanField(default=False)
