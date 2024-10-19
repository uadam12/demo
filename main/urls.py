from django.urls import path
from . import views

app_name = 'main'

"""
# Requirements
def requirements(request):
    return details_view(
        request, RequirementForm, 
        header="Requirement",
        data_template="board/requirements.html",
        requirements = Requirement.objects.order_by('label')
    )

def update_requirement(request, id):
    requirement = Requirement.objects.get(id=id)
    
    return update_view(
        request, 
        model=requirement, 
        form_class=RequirementForm, 
        success_url='board:requirements', 
        header='Requirement'
    )

    
def delete_requirement(request, id):
    requirement = Requirement.objects.get(id=id)
    
    return delete_view(
        request, 
        model=requirement,
        success_url='board:requirements', 
        header='Requirement'
    )
"""

urlpatterns = [
    path('', views.index, name='home'),
    path('news/', views.news, name='news'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Articles
    path('articles/', views.articles, name='articles'),
    path('news/<int:id>', views.article, name='article'),
    path('articles/create', views.create_article, name='create-article'),
    path('articles/<int:id>/update', views.update_article, name='update-article'),
    path('articles/<int:id>/delete', views.delete_article, name='delete-article'),
]
