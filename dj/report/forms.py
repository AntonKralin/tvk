from django import forms
from tvk.models import Imns


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