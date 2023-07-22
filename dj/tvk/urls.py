from django.urls import path
from . import views

app_name = 'tvk'

urlpatterns = [
    path('main', views.main, name='main'),
    path('main/<int:page>', views.main, name='p_main'),
    path('cic', views.cic, name='cic'),
    path('cic/<int:id>', views.cic, name='edit_cic'),
    path('save_cic', views.save_cic, name='save_cic'),
    path('department', views.department, name='department'),
    path('department/<int:id>', views.department, name='edit_department'),
    path('save_department', views.save_department, name='save_department'),
    path('delete_department/<int:id>', views.delete_department, name='delete_department'),
    path('risk', views.risk, name='risk'),
    path('risk/<int:id>', views.risk, name='edit_risk'),
    path('save_risk', views.save_risk, name='save_risk'),
    path('upload_file', views.upload_file, name='upload_file'),
    path('delete_risk/<int:id>', views.delete_risk, name='delete_risk'),
    path('imns', views.imns, name='imns'),
    path('imns/<int:id>', views.imns, name='edit_imns'),
    path('save_imns', views.save_imns, name='save_imns'),
    path('delete_imns/<int:id>', views.delete_imns, name='delete_imns'),
]