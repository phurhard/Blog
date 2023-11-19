from django.shortcuts import render, redirect
from .forms import RegisterForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from .models import Article
# Create your views here.


@login_required(login_url='/login')
def home(request):
    return render(request, 'main/index.html')

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()
        
    return render(request, 'registration/sign_up.html', {'form': form})

@login_required(login_url='/login')
def post(request):
    """This view creates a new post"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/articles')
    else:
        form = PostForm()
    return render(request, 'main/post.html', {'form': form})

@login_required(login_url='/login')
def articles(request):
    """This view returns a list of all the posts in the db"""
    articles = Article.objects.all()
    
    if request.method == "POST":
        post_id = request.POST.get('post-id')
        post = Article.objects.filter(id=post_id).first()
        if post and request.user == post.author:
            post.delete()
    return render(request, 'main/articles.html', {'articles': articles})
