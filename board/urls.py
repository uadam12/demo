from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    # Requirements
    path('requirements/', views.requirements, name='requirements'),
    path('requirements/create', views.create_requirement, name='create-requirement'),
    path('requirements/<int:id>/update/', views.update_requirement, name='update-requirement'),
    path('requirements/<int:id>/delete/', views.delete_requirement, name='delete-requirement'),

    # Criteria
    path('criteria/', views.criteria, name='criteria'),
    path('criteria/create/', views.create_criterion, name='create-criterion'),
    path('criteria/<int:id>/update/', views.update_criterion, name='update-criterion'),
    path('criteria/<int:id>/delete/', views.delete_criterion, name='delete-criterion'),

    # Banks
    path('banks/', views.banks, name='banks'),
    path('banks/create/', views.create_bank, name='create-bank'),
    path('banks/<str:code>/', views.bank, name='bank'),
    path('banks/<str:code>/update/', views.update_bank, name='update-bank'),
    path('banks/<str:code>/delete/', views.delete_bank, name='delete-bank'),
    
    # Local Government Area(LGA)
    path('lgas/', views.lgas, name='lgas'),
    path('lgas/create/', views.create_lga, name='create-lga'),
    path('lgas/<str:code>/update/', views.update_lga, name='update-lga'),
    path('lgas/<str:code>/delete/', views.delete_lga, name='delete-lga'),
]
