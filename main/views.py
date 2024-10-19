from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from app import render, is_post
from app.views import create_view, update_view, delete_view
from .forms import Article, ArticleForm, ContactForm


def index(request):
    return render(request, 'main/index')

def news(request):
    articles = Article.objects.all()
    pagenator = Paginator(articles, 10, 4)
    page = request.GET.get('page', 1)
    articles = pagenator.get_page(page)
    
    return render(request, 'main/news', articles=articles)

def about(request):
    return render(request, 'main/about')

def contact(request):
    if is_post(request):
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            
            messages.success(request, 'Message sent successfully!')
            return redirect('user:dashboard')
            
    else:form = ContactForm()
    
    return render(request, 'main/contact', form=form)
    
# Articles
def articles(request):
    return render(
        request, "main/articles",
        title='BSSB | Articles/News',
        articles = Article.objects.all()
    )
    
def article(request, id):
    article = get_object_or_404(Article, id=id)
    return render(
        request, 'main/article',
        title = article.headline,
        article = article
    )

def create_article(request):
    return create_view(
        request, form_class=ArticleForm, 
        success_url='main:articles', 
        header='Create Article'
    )

def update_article(request, id):
    article = get_object_or_404(Article, id=id)

    return update_view(
        request, instance=article,
        form_class=ArticleForm, 
        success_url='main:articles', 
        header='Update Article'
    )
    
def delete_article(request, id):
    article = get_object_or_404(Article, id=id)
    
    return delete_view(
        request, model=article,
        success_url='main:articles', 
        header='Local Government Area'
    )