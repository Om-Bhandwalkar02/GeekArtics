from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from articles.forms import ArticleForm, UserRegisterForm
from django.contrib.auth import login
from articles.models import Article


# Create your views here.
def articles(request):
    queryset = Article.objects.all().order_by('-pub_date')
    if request.user.is_authenticated:
        username = request.user.username
        username = "Welcome " + username + "!"
    else:
        username = "Welcome! Please login to create an article!"
    return render(request, 'articles/article-list.html', context={'articles': queryset, 'username': username})


@login_required()
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('home')
    else:
        form = ArticleForm()
    return render(request, 'articles/article-form.html', context={'form': form})


@login_required()
def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/article-form.html', context={'form': form})


@login_required()
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk, user=request.user)
    if request.method == 'POST':
        article.delete()
        return redirect('articles')
    return render(request, 'articles/article-confirm-delete.html', context={'article': article})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('articles')

    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', context={'form': form})


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    context = {'article': article}
    return render(request, 'articles/article-detail.html', context)
