from django.urls import path
from . import views

app_name = 'report'

urlpatterns = [
    path('choose_period', views.choose_period, name='choose_period'),
    path('report', views.report, name='report'),
    path('contraventions', views.contraventions, name='contraventions'),
]