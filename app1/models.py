from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import Group


class Departments(models.Model):
    name=models.CharField(max_length=50)
    diagnostics=models.CharField(max_length=100,blank=True,null=True)
    location=models.CharField(max_length=100,blank=True,null=True)
    specialization=models.CharField(max_length=100,blank=True,null=True)
    
    def __str__(self):
        return (str(self.name) + str(self.id))
    
    
class User(AbstractUser):
    name=models.CharField(max_length=255, blank=True ,null=True)
    usertype=models.CharField(max_length=255,null=True,blank=True)
    departments=models.ForeignKey(Departments,on_delete=models.CASCADE,null=True,blank=True)

    class meta:
        verbose_name='User'
        verbose_name_plural='Users'
        
    def __str__(self):
        return (str(self.name) + str(self.id))
    

        
class Patient_Records(models.Model):
    patient_id=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateTimeField(default=timezone.now)
    observations=models.CharField(max_length=500,blank=True,null=True)
    treatments=models.CharField(max_length=500,blank=True,null=True)
    departments=models.ForeignKey(Departments,on_delete=models.CASCADE)
    
