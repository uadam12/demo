from django.urls import path
from . import views, application_views as app_views

app_name = 'scholarship'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_scholarship, name='create'),
    path('<int:id>/', views.scholarship, name='scholarship'),
    path('<int:id>/update/', views.update_scholarship, name='update'),
    path('<int:id>/delete/', views.delete_scholarship, name='delete'),
    path('<int:id>/add-program/', views.add_scholarship_program, name='add-program'),
    path('programs/<int:id>/update/', views.update_scholarship_program, name='update-program'),
    path('programs/<int:id>/delete/', views.delete_scholarship_program, name='delete-program'),

    path('internals/', views.internal_scholarships, name='internals'),
    path('externals/', views.external_scholarships, name='externals'),
    path('applications/', app_views.applications, name='applications'),
    path('applications/<int:id>', app_views.scholarship_applications, name='scholarship-applications'),
    path('applications/<str:application_id>', app_views.application, name='application'),
]
