from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.contrib.auth import get_user_model
from django.utils import timezone
from .forms import PostForm,CreateUserForm
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
# Create your views here.


def logedin(request):
        if request.user.is_authenticated:
            return redirect('post_list')
        else:
                if request.method == 'POST':
                    username = request.POST.get('username')
                    password =request.POST.get('password')

                    user = authenticate(request, username=username, password=password)
                    # return HttpResponse(login(request))
                    if user is not None:
                        login(request,user)
                        return redirect('post_list')
                    else:
                        messages.info(request, 'Username OR password is incorrect')

                return render(request, 'blog/login.html',{})


def register(request):
        if request.user.is_authenticated:
            return redirect('post_list')
        else:
            form = CreateUserForm()
            if request.method == 'POST':
                    form = CreateUserForm(request.POST)
                    if form.is_valid():
                        form.save()
                        user = form.cleaned_data.get('username')
                        messages.success(request, 'Account was created for ' + user)

                        return redirect('login')
                    

            return render(request, 'blog/register.html',{'form':form})

@login_required(login_url='login')
def post_list(request):
        posts = Post.objects.filter(published_date__lte=timezone.now()).filter(author=request.user).order_by('published_date')
        return render(request, 'blog/post_list.html', {'posts': posts})

@login_required(login_url='login')
def post_list_up(request):
        posts = Post.objects.exclude(published_date__lte=timezone.now()).filter(author=request.user).order_by('published_date')
        # return HttpResponse(posts)
        return render(request, 'blog/post_list_up.html', {'posts': posts})

@login_required(login_url='login')
def logedout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def post_detail(request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', {'post': post})

# def post_new(request):
#     form = PostForm()
#     # return HttpResponse(form)
#     return render(request, 'blog/post_edit.html', {'form': form})

@login_required(login_url='login')
def post_new(request):
        if request.method == "POST":
            form = PostForm(request.POST)
            User = get_user_model()
            # return HttpResponse(User.objects.first())
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                # post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

@login_required(login_url='login')
def post_edit(request, pk, published):
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            User = get_user_model()
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user 
                if published == 1:
                    post.published_date = timezone.now()
                post.save()
                # return HttpResponse(post.published_date)
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
            # return HttpResponse(post.published_date)
        return render(request, 'blog/post_edit.html', {'form': form,'post':post})
