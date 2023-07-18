from django.contrib import admin
from .models import CIC, Department, Imns, Risk


# Register your models here.
admin.site.register(CIC)
admin.site.register(Department)
admin.site.register(Imns)
admin.site.register(Risk)