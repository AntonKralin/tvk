from django import forms
from .models import Department, Risk, Imns, CIC
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
    name = forms.CharField(label='Название', widget=forms.TextInput(attrs={
        'placeholder':'Название',
        'class':'form-control'
    }))
    description = forms.CharField(label='Описание риска', widget=forms.Textarea(attrs={
        'placeholder':'Описание',
        'class':'form-control'
    }))
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
    obj = forms.ModelMultipleChoiceField(label='Код ИМНС объекта(кого проверяют)',
                                         queryset=Imns.objects.order_by('number'))
    number = forms.CharField(label='№ утвержденного отчета', widget=forms.TextInput(attrs={
        'placeholder':'№ утвержденного отчета',
        'class':'form-control'
    }))
    date_state = forms.DateField(label='Дата утвержденного отчета', initial=datetime.date.today,
                                 widget=forms.DateInput(format = '%Y-%m-%d',attrs={'type': 'date'}))
    date_from = forms.DateField(label='Изучаемый периуд с', initial=datetime.date.today,
                                 widget=forms.DateInput(format = '%Y-%m-%d',attrs={'type': 'date'}))
    date_to = forms.DateField(label='Изучаемый периуд по', initial=datetime.date.today,
                                 widget=forms.DateInput(format = '%Y-%m-%d',attrs={'type': 'date'}))
    risk = forms.ModelChoiceField(label='Код риска',
                                   queryset=Risk.objects.filter(enable=True).order_by('code'))
    count_all = forms.IntegerField(label='Количество документов(фактов), подвергнутых контролю', widget=forms.TextInput(attrs={
        'placeholder':'Количество документов(фактов), подвергнутых контролю',
        'class':'form-control'
    }))
    count_contravention = forms.IntegerField(label='Количество документов(фактов), в отношении которых установлены нарушения', widget=forms.TextInput(attrs={
        'placeholder':'Количество документов(фактов), в отношении которых установлены нарушения',
        'class':'form-control'
    }))
    point = forms.CharField(label='Краткое содержание(суть), нарушения', widget=forms.Textarea(attrs={
        'placeholder':'Краткое содержание(суть), нарушения',
        'class':'form-control',
        'rows' : '3'
    }))
    departments = forms.ModelMultipleChoiceField(label='Код ИМНС объекта(кого проверяют)',
                                         queryset=Department.objects.all())
    class Meta:
        model = CIC
        fields = ['id', 'imnss', 'obj', 'number', 'date_state', 'date_from', 
                  'date_to', 'risk', 'count_all', 'count_contravention', 'point', 'departments']
        

class FilterForm(forms.Form):
    number = forms.IntegerField(initial=None, required=False, widget=forms.TextInput(attrs={
        'size': '1'
    }))
    imnss = forms.CharField(initial=None, required=False, widget=forms.TextInput(attrs={
        'size': '1'
    }))
    report = forms.CharField(initial=None, required=False, widget=forms.TextInput(attrs={
        'size': '4'
    }))
    date_state = forms.DateField(initial=None, required=False, 
                                 widget=forms.DateInput(format = '%Y-%m-%d',attrs={'type': 'date'}))
    date_from = forms.DateField(initial=None, required=False, 
                                 widget=forms.DateInput(format = '%Y-%m-%d',attrs={'type': 'date'}))
    date_to = forms.DateField(initial=None, required=False, 
                                 widget=forms.DateInput(format = '%Y-%m-%d',attrs={'type': 'date'}))
    code = forms.CharField(initial=None, required=False, widget=forms.TextInput(attrs={
        'size': '1'
    }))
    count_all = forms.IntegerField(initial=None, required=False, widget=forms.TextInput(attrs={
        'size': '3'
    }))
    count_con = forms.IntegerField(initial=None, required=False, widget=forms.TextInput(attrs={
        'size': '3'
    }))
    department = forms.CharField(initial=None, required=False, widget=forms.TextInput(attrs={
        'size': '15'
    }))