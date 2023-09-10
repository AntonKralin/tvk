from django.db import models
from django.contrib.auth.models import AbstractUser
from .const import access
from tvk.models import Imns


# Create your models here.
class User(AbstractUser):
    access = models.IntegerField(choices=access, blank=True, null=True)
    imns = models.ForeignKey(Imns, verbose_name='Инспекция', 
                             on_delete=models.PROTECT, 
                             blank=True, null=True)

    def __str__(self):
        return str(self.username)
