from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('jobs/<int:job_id>/', views.apply_job, name='job_apply'),
    path('login/', views.AdminLoginView.as_view(), name='admin_login'),
    path('logout/', views.AdminLogoutView.as_view(), name='admin_logout'),
    path('jobs/', views.job_list, name='job_list'),

]
