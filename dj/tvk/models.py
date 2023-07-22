from django.db import models
from django.urls import reverse


# Create your models here.
class Risk(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    enable = models.BooleanField(default=True)
    
    objects = models.Manager()
    
    def __str__(self) -> str:
        return self.code
    

class Department(models.Model):
    name = models.CharField(max_length=255)
    objects = models.Manager()
    
    def __str__(self):
        return str(self.name)    
    
    
class Imns(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=255)
    shot_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    post = models.CharField(max_length=255, blank=True, null=True)
    unp = models.CharField(max_length=255, blank=True, null=True)
    
    objects = models.Manager()
    
    def __str__(self) -> str:
        return str(self.number) + " " + self.shot_name

    
    
class CIC(models.Model):
    imnss = models.ForeignKey(Imns, on_delete=models.CASCADE)
    obj = models.ManyToManyField(Imns, related_name='obj')
    number = models.CharField(max_length=255, blank=True, null=True)
    date_state = models.DateField()
    date_from = models.DateField()
    date_to = models.DateField()
    risk = models.ManyToManyField(Risk)
    count_all = models.IntegerField()
    count_contravention = models.IntegerField(blank=True, null=True)
    point = models.TextField(blank=True, null=True)
    departments = models.ManyToManyField(Department)
    
    objects = models.Manager()
    
    def __str__(self) -> str:
        return "id:" + str(self.id)
    
    
    
