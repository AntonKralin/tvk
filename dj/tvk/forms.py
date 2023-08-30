from django import forms
from django.db.models import F
from .models import Department, Risk, Imns, CIC, Examination
import datetime


class DepartmentsForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput(), initial='', required=False)
    name = forms.CharField(label='Название', widget=forms.TextInput(attrs={
        'placeholder':'Название',
        'class':'form-control'
    }))
    class Meta:
        model = Department
        fields = ['id', 'name']
        
        
class RiskForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput(), initial='', required=False)
    code = forms.CharField(label='Код риска', widget=forms.TimeInput(attrs={
        'placeholder':'Код',
        'class':'form-control'
    }))
    name = forms.CharField(label='Название', widget=forms.Textarea(attrs={
        'placeholder':'Название',
        'class':'form-control'
    }))
    description = forms.CharField(label='Описание риска', widget=forms.Textarea(attrs={
        'placeholder':'Описание',
        'class':'form-control'
    }), required=False)
    enable = forms.BooleanField(label='Активен', initial=True, required=False)
    class Meta:
        model = Risk
        fields = ['id', 'code', 'name', 'description', 'enable']
        
        
class IMNSForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput(), required=False, initial='')
    number = forms.IntegerField(label='Номер инспекции', widget=forms.TextInput(attrs={
        'placeholder':'Номер инспекции',
        'class':'form-control'
    }))
    name = forms.CharField(label='Полное название инспекции', widget=forms.TextInput(attrs={
        'placeholder':'Полное название инспекции',
        'class':'form-control'
    }))
    shot_name = forms.CharField(label='Короткое название инспекции', widget=forms.TextInput(attrs={
        'placeholder':'Короткое название инспекции',
        'class':'form-control'
    }))
    address = forms.CharField(label='Адресс инспекции', widget=forms.TextInput(attrs={
        'placeholder':'Адресс инспекции',
        'class':'form-control'
    }))
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={
        'placeholder':'Email',
        'class':'form-control'
    }))
    post = forms.CharField(label='Почта', widget=forms.TextInput(attrs={
        'placeholder':'Почта',
        'class':'form-control'
    }))
    unp = forms.CharField(label='УНП', widget=forms.TextInput(attrs={
        'placeholder':'УНП',
        'class':'form-control'
    }))
    
    class Meta:
        model = Imns
        fields = ['id', 'number', 'name', 'shot_name', 'address', 'email', 'post', 'unp']
        
        
class CICForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput(), required=False, initial='')
    imnss = forms.ModelChoiceField(label='Код ИМНС субъекта(кто проверяет)',
                                   queryset=Imns.objects.order_by('number'))
    number = forms.CharField(label='№ утвержденного отчета', widget=forms.TextInput(attrs={
        'placeholder':'№ утвержденного отчета',
        'class':'form-control'
    }))
    date_state = forms.DateField(label='Дата утвержденного отчета', initial=datetime.date.today,
                                 widget=forms.DateInput(format = '%Y-%m-%d',attrs={'type': 'date'}))
    date_from = forms.DateField(label='Изучаемый период с', initial=datetime.date.today,
                                 widget=forms.DateInput(format = '%Y-%m-%d',attrs={'type': 'date'}))
    date_to = forms.DateField(label='Изучаемый период по', initial=datetime.date.today,
                                 widget=forms.DateInput(format = '%Y-%m-%d',attrs={'type': 'date'}))
    message = forms.CharField(label='Направлено обзорное письмо', widget=forms.TextInput(attrs={
                                  "placeholder": 'Направлено обзорное письмо',
                                  'class': 'form-control'
                                  }), required=False, initial=None)

    class Meta:
        model = CIC
        fields = ['id', 'imnss', 'number', 'date_state', 'date_from', 
                  'date_to', 'message']
        
class ExaminationForm(forms.ModelForm):
    id = forms.CharField(initial='', widget=forms.HiddenInput(), required=False)
    cic = forms.IntegerField(widget=forms.HiddenInput())
    obj = forms.ModelChoiceField(label='Объект', queryset=Imns.objects.order_by('number').exclude(number=300))
    risk = forms.ModelChoiceField(label='Риск', queryset=Risk.objects.order_by('code').exclude(enable=False))
    department = forms.ModelChoiceField(label='Подразделение', queryset=Department.objects.all())
    count_all = forms.IntegerField(label='Количество документов подвегрнутых контролю', 
                                   widget=forms.TextInput(attrs={
                                    "placeholder": 'Количество документов подвегрнутых контролю',
                                    'class': 'form-control'
                                    }))
    count_contravention = forms.IntegerField(label='Количество нарушений', widget=forms.TextInput(attrs={
                                            "placeholder": 'Количество документов подвегрнутых контролю',
                                            'class': 'form-control'
                                            }), initial=0)
    description = forms.CharField(label='Краткое содержание нарушения', widget=forms.Textarea(attrs={
                                'placeholder':'Краткое содержание нарушения',
                                'class':'form-control'
                                }), required=False)
    
    class Meta:
        model = Examination
        fields = ['id', 'cic', 'obj', 'risk', 'department', 'count_all', 
                  'count_contravention', 'description']
        
        
class FilterMainForm(forms.Form):
    subject = forms.ModelChoiceField(label='Субъект', queryset=Imns.objects.order_by('number'), 
                                     widget=forms.Select(attrs={
                                        'onchange': "this.form.submit()"
                                    }), required=False)
    year = forms.ChoiceField(label='год', widget=forms.Select(attrs={
                                'onchange': "this.form.submit()"
                            }), required=False,
                            choices=[(year, year) for year in range(datetime.datetime.now().year, 2021, -1 )])
        

class UploadRiskFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'accept': ".csv"}))
     