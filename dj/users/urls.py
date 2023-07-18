from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('login', views.login, name='login'),
    path('users', views.users, name='users'),
    path('user/<int:id>', views.users, name='change_user'),
    path('save_user', views.save_user, name='save_user'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),
    path('clearsession', views.clear_session, name='clearsession'),
]


