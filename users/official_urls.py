from django.urls import path
from . import official_views as views

app_name = 'official'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admins/', views.admins, name='admins'),
    path('admins/<int:id>/', views.delete_admin, name='delete-admin'),
    path('admins/create/', views.create_admin, name='create-admin'),
    path('guests/', views.guests, name='guests'),
    path('admins/<int:id>/', views.delete_guest, name='delete-guest'),
    path('guests/create', views.create_guest, name='create-guest'),
    path('applicants/', views.applicants, name='applicants'),
    path('applicants/<int:applicant_id>/block', views.block_applicant, name='block-applicant'),
    path('applicants/<int:applicant_id>/unblock', views.unblock_applicant, name='unblock-applicant'),
    
]