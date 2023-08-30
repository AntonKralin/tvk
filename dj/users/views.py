from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserSaveForm
from .models import User
from tvk.models import Imns
from .const import access_r


# Create your views here.
def index(request:HttpRequest):
    """index page"""
    if request.method == 'GET':
        id_user = request.session.get('id_user', None)
        if id_user:
            return redirect("tvk:main")
    context = {"form": UserLoginForm()}
    return render(request, 'users/index.html', context=context)

def login(request:HttpRequest):
    """login page"""
    if request.method == "POST":

        message = ''
        login = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if not login and not password:
            message = 'Введите логин и пароль'
        else:
            user = auth.authenticate(username=login, password=password)
            if user:
                auth.login(request, user)
                return redirect('tvk:main')
            else:
                message = 'Неправильный логин или пароль'

        context = {'message': message,
                   'form': UserLoginForm()}
        return render(request, 'users/index.html', context=context)


@login_required    
def users(request:HttpRequest, id:int=None):
    """users page"""
    user = request.user

    user_form = UserSaveForm()

    if id is not None:
        user_edit = User.objects.get(id=id)
        user_form = UserSaveForm(instance=user_edit)

    user_list = []
    if user.access == 1:
        user_form.fields['imns'].queryset = Imns.objects.all()
        user_list = User.objects.all()
    else:
        user_form.fields['imns'].queryset = Imns.objects.filter(id=user.imns.id)
        user_form.fields['access'].choices = access_r
        user_list = User.objects.filter(imns=user.imns)

    context = {'user': user,
               'form': user_form,
               'user_list': user_list}
    return render(request, 'users/users.html', context=context)


@login_required
def save_user(request:HttpRequest):
    """save_user page"""
    if request.method == "POST":
        id = request.POST.get('id', '')
        if id != '':
            user = User.objects.get(id=id)
            user_form = UserSaveForm(instance=user, data=request.POST)
            username = request.POST.get('username')
            pass1 = request.POST.get('password1')
            pass2 = request.POST.get('password2')
            access = request.POST.get('access')
            imns = Imns.objects.get(id=request.POST.get('imns'))
            if pass1 == pass2 and pass1 != '':
                user.username = username
                user.access = access
                user.imns = imns
                user.save()
                user.set_password(pass1)
                user.save()
                return redirect('users:users')
        else:
            user_form = UserSaveForm(data=request.POST)
        if user_form.is_valid():
            user_form.save()
        else:
            return HttpResponse('Не верно заполнена форма' + str(user_form.errors))

    return redirect('users:users')


@login_required
def delete_user(request:HttpRequest, id:int=None):
    """delete_user page"""
    if request.method == "GET" and id:
        del_user = User.objects.get(id=id)
        del_user.delete()
    return redirect('users:users')


def clear_session(request:HttpRequest):
    """clear session"""
    request.session.clear()
    request.session.modified = True
    auth.logout(request)
    return redirect("users:index")
