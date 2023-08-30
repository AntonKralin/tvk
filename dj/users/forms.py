from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .models import User
from .const import access
from tvk.models import Imns


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Логин',
        'class':'form-control'
    }), label='Логин')
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Пароль'
    }), label='Пароль')
    class Meta:
        model = User
        fields = ['username', 'password']


class UserSaveForm(UserCreationForm):
    id = forms.CharField(widget=forms.HiddenInput, required=False, initial='')
    username = forms.CharField(widget=forms.TimeInput(attrs={
        'placeholder':'Логин',
        'class':'form-control'
    }), label='Логин')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Пароль'
    }), label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Пароль'
    }), label='Повторите пароль')
    access = forms.ChoiceField(choices=access, label='Доступ')
    imns = forms.ModelChoiceField(label='Инспекция', queryset=Imns.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'password1', 'password2', 'access', 'imns']
    