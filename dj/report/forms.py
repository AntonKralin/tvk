from django import forms


class ChoosePeriodForm(forms.Form):
    date_from = forms.DateField(label='Период с', required=False, initial=None,
                                widget=forms.DateInput(format = '%Y-%m-%d',attrs={'type': 'date'}))
    date_to = forms.DateField(label='Период по', required=False, initial=None,
                              widget=forms.DateInput(format = '%Y-%m-%d',attrs={'type': 'date'}))