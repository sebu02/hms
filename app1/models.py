from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    name=models.CharField(max_length=255, blank=True ,null=True)
    
    class meta:
        verbose_name='User'
        verbose_name_plural='Users'
        
class Departments(models.Model):
    department_id=models.IntegerField(unique=True)
    name=models.CharField(max_length=50)
    diagnostics=models.CharField(max_length=100,blank=True,null=True)
    location=models.CharField(max_length=100,blank=True,null=True)
    specialization=models.CharField(max_length=100,blank=True,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
         
class Patient_Records(models.Model):
    record_id=models.IntegerField(unique=True)
    patient_id=models.IntegerField(unique=True)
    created_date=models.DateTimeField(default=timezone.now)
    observations=models.CharField(max_length=500,blank=True,null=True)
    treatments=models.CharField(max_length=500,blank=True,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    departments=models.ForeignKey(Departments,on_delete=models.CASCADE)
