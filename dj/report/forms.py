from django import forms
from tvk.models import Imns, Risk, Department


class ChoosePeriodForm(forms.Form):
    date_from = forms.DateField(label='Период с', required=False, initial=None,
                                widget=forms.DateInput(format = '%Y-%m-%d',attrs={'type': 'date'}))
    date_to = forms.DateField(label='Период по', required=False, initial=None,
                              widget=forms.DateInput(format = '%Y-%m-%d',attrs={'type': 'date'}))
    
    
class FilterForm(forms.Form):
    subject = forms.ModelChoiceField(label='Субъект', queryset=Imns.objects.order_by('number'), 
                                     widget=forms.Select(attrs={
                                        'onchange': "this.form.submit()"
                                    }), required=False)
    obj = forms.ModelChoiceField(label='Объект', queryset=Imns.objects.order_by('number').exclude(number=300), 
                                     widget=forms.Select(attrs={
                                        'onchange': "this.form.submit()"
                                    }), required=False)
    risk = forms.ModelChoiceField(label='Риск', queryset=Risk.objects.order_by('code').exclude(enable=False), widget=forms.Select(attrs={
                                        'onchange': "this.form.submit()"
                                    }), required=False)
    department = forms.ModelChoiceField(label='Подразделение', queryset=Department.objects.all(), widget=forms.Select(attrs={
                                            'onchange': "this.form.submit()"
                                        }), required=False)
    

class CheckingFilterForm(forms.Form):
    subject = forms.ModelChoiceField(label='Субъект', queryset=Imns.objects.order_by('number'), 
                                     widget=forms.Select(attrs={
                                        'onchange': "this.form.submit()"
                                    }), required=False)
    risk = forms.ModelChoiceField(label='Риск', queryset=Risk.objects.order_by('code').exclude(enable=False), widget=forms.Select(attrs={
                                        'onchange': "this.form.submit()"
                                    }), required=False)
    department = forms.ModelChoiceField(label='Подразделение', queryset=Department.objects.all(), widget=forms.Select(attrs={
                                            'onchange': "this.form.submit()"
                                        }), required=False)