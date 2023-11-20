from django.shortcuts import render, redirect
from .forms import RegisterForm, PostForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login
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
@permission_required('main.add_article',
                     login_url='/login', raise_exception=True)
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
        user_id = request.POST.get('user-id')
        if post_id:
            post = Article.objects.filter(id=post_id).first()
            if post and (request.user == post.author or
                         request.user.has_perm('main.delete_article')):
                post.delete()
        elif user_id:
            user = User.objects.filter(id=user_id).first()
            if user and (request.user.is_staff):
                try:
                    group = Group.objects.get(name='default')
                    group.user_set.remove(user)
                except Exception:
                    pass
                try:
                    group = Group.objects.get(name='moderator')
                    group.user_set.remove(user)
                except Exception:
                    pass
    return render(request, 'main/articles.html', {'articles': articles})
