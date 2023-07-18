from django.db import models
from django.urls import reverse


# Create your models here.
class Risk(models.Model):
    code = models.CharField(max_length=50, verbose_name='Код риска',
                            help_text='Введите код риска')
    name = models.CharField(max_length=255, verbose_name='Название риска',
                            help_text='Введите название риска')
    description = models.TextField(verbose_name='Описание', 
                                   help_text='Введите описание', blank=True, null=True)
    enable = models.BooleanField(verbose_name='Активен',
                                 help_text='Активен', default=True)
    
    objects = models.Manager()
    
    def __str__(self) -> str:
        return self.code
    

class Department(models.Model):
    name = models.CharField(max_length=255, verbose_name='Назнавание', 
                            help_text='Введите название')
    objects = models.Manager()
    
    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse("department-detail", args=[str(self.id)])
    
    
    
class Imns(models.Model):
    number = models.IntegerField(verbose_name='Номер инспекции', 
                                 help_text='Введите номер инспекции')
    name = models.CharField(max_length=255, verbose_name='Полное наименование инспекции',
                            help_text='Введите полное наименование инспекции')
    shot_name = models.CharField(max_length=255, verbose_name='Короткое название инспекции',
                                 help_text='Введите короткое название инспекции')
    address = models.CharField(max_length=255, verbose_name='Адресс инспекции',
                               help_text='Введите адресс инспекции', blank=True, null=True)
    email = models.CharField(max_length=255, verbose_name='Email', 
                            help_text='Введите email', blank=True, null=True)
    post = models.CharField(max_length=255, verbose_name='Почтовый индекс', 
                            help_text='Введите почтовый индекс', blank=True, null=True)
    unp = models.CharField(max_length=255, verbose_name='УНП', 
                           help_text='Введите УНП', blank=True, null=True)
    
    objects = models.Manager()
    
    def __str__(self) -> str:
        return str(self.number) + " " + self.shot_name

    
    
class CIC(models.Model):
    imnss = models.ForeignKey(Imns, on_delete=models.CASCADE, 
                             verbose_name='Код ИМНС субъекта(кто проверяет)', 
                             help_text='Код ИМНС субъекта(кто проверяет)')
    obj = models.ManyToManyField(Imns, help_text='Код ИМНС объекта(кого проверяют)',
                                     verbose_name='Код ИМНС объекта(кого проверяют)',
                                     related_name='obj')
    number = models.CharField(max_length=255, verbose_name='№ утвержденного отчета',
                              help_text='Введите номер утвержденного отчета', 
                              blank=True, null=True)
    date_state = models.DateField(verbose_name='Дата утвержденного отчета',
                                  help_text='Введите дату утвержденного отчета')
    date_from = models.DateField(verbose_name='Изучаемый периуд с',
                                 help_text="C")
    date_to = models.DateField(verbose_name='Изучаемый периуд по',
                                 help_text="По")
    risk = models.ForeignKey(Risk, on_delete=models.CASCADE, 
                             verbose_name='Код риска')
    count_all = models.IntegerField(verbose_name='Количество документов(фактов), подвергнутых контролю',
                                    help_text='Введите количество документов подвергнутых контролю')
    count_contravention = models.IntegerField(verbose_name='Количество документов(фактов), в отношении которых установлены нарушения',
                                              help_text='Введите количетво докуметов, в отношении которых установлены нарушения',
                                              blank=True, null=True)
    point = models.TextField(verbose_name='Краткое содержание(суть), нарушения', 
                             help_text='Введите суть нарушения', blank=True, null=True)
    departments = models.ManyToManyField(Department, verbose_name='Подразделение проводившее ТВК')
    
    objects = models.Manager()
    
    
    
