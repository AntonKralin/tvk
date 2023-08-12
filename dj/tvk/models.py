from django.db import models
from django.urls import reverse


# Create your models here.
class Risk(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.TextField()
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
    imnss = models.ForeignKey(Imns, on_delete=models.PROTECT)
    number = models.CharField(max_length=255, blank=True, null=True)
    date_state = models.DateField()
    date_from = models.DateField()
    date_to = models.DateField()
    message = models.CharField(max_length=255, blank=True, null=True)
    
    objects = models.Manager()
    
    def __str__(self) -> str:
        return "id:" + str(self.id)
    
    
class Examination(models.Model):
    obj = models.ForeignKey(Imns, on_delete=models.PROTECT)
    risk = models.ForeignKey(Risk, on_delete=models.PROTECT)
    cic  = models.ForeignKey(CIC, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    count_all = models.IntegerField()
    count_contravention = models.IntegerField()
    description = models.TextField(blank=True, null=True)    
    
    objects = models.Manager()
    
    def __str__(self) -> str:
        return "id:" + str(self.id)
