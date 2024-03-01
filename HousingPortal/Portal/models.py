from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

# Create your models here.


# class UserAccount(AbstractUser):
#     username = models.CharField(max_length=50, editable=True, unique=True)
#     email = models.EmailField(primary_key=True, unique=True)
#     password = models.CharField(max_length=100)
#     admin = models.BooleanField(default=False)
#     twoFactorKey = models.CharField(max_length=100)
#     manager = models.OneToOneField('Manager', on_delete=models.SET_NULL, null=True, blank=True)
#     tenant = models.OneToOneField('Tenant', on_delete=models.SET_NULL, null=True, blank=True)
#     userHousingApplications = models.ManyToManyField('HousingApplication', through='UserHousingApplication')
#     maintenanceRequest = models.ForeignKey('MaintenanceRequest', on_delete=models.CASCADE, null=True)
#     archived = models.BooleanField(default=False)

#     def save(self, *args, **kwargs):
#         if not self.username:
#             self.username = self.email
#         super(UserAccount, self).save(*args, **kwargs)

class UserAccount(AbstractUser): 
    # AbstractUser has fields: id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined
    twoFactorKey = models.CharField(max_length=100)
    manager = models.OneToOneField('Manager', on_delete=models.SET_NULL, null=True, blank=True)
    tenant = models.OneToOneField('Tenant', on_delete=models.SET_NULL, null=True, blank=True)
    #userHousingApplications = models.ManyToManyField('HousingApplication', through='UserHousingApplication')
    archived = models.BooleanField(default=False)



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
    unitFloor = models.CharField(max_length=100)
    unitSize = models.CharField(max_length=100)
    unitName = models.CharField(max_length=100)
    unitBedrooms = models.CharField(max_length=100)


class MaintenanceRequest(models.Model):
    unitId = models.ForeignKey('Unit', null=True, on_delete=models.CASCADE) # Take out null=True when Unit is working
    userId = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    request = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)


class UserHousingApplication(models.Model):
    userId = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
    housingApplicationId = models.ForeignKey('HousingApplication', on_delete=models.CASCADE)


class HousingApplication(models.Model):
    accepted = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    unit_wanted = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
