from django.urls import path
from . import views

app_name = 'report'

urlpatterns = [
    path('choose_period', views.choose_period, name='choose_period'),
    path('report', views.report, name='report'),
    path('contraventions', views.contraventions, name='contraventions'),
    path('contraventions/<int:page>', views.contraventions,
         name='p_contraventions'),
    path('checking', views.checking, name='checking'),
    path('checking/<int:page>', views.checking, name='p_checking'),
]
