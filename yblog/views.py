from django.shortcuts import render, redirect
from .models import Post, Comment, Preference
from operator import attrgetter
from django.http import HttpResponse
from .forms import PostForm, NewUserForm, CommentForm, ImageFormSet
from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator #bring the paginator
# Create your views here.

def homepage(request): #has the list of posts
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    pref_posts = Post.objects.filter(likes__gt=0).order_by('-likes')
    return render(request,'yblog/home.html',{'posts':posts, 'pref_posts':pref_posts}) #send the posts queries to the homepage

def post_all(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    ####
    paginator = Paginator(posts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    ####
    return render(request, 'yblog/post_all.html',{'posts':page_obj})

def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"회원가입이 완료되었습니다: {username}")
            messages.info(request, f"환영합니다. {username} 학우님 ")
            login(request, user)
            return redirect('/')
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
    form = NewUserForm()
    return render(request, 'yblog/register.html',{'form':form})

def logout_request(request):
    logout(request)
    messages.info(request, "로그아웃 하였습니다.")
    return redirect("/")

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"안녕하세요 {username} 학우님")
                return redirect("/")
            else:
                messages.error(request, "잘못된 아이디나 비밀번호입니다.")

    form = AuthenticationForm()
    return render(request, "yblog/login.html", {'form':form})
"""
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user #set the current user to author
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail",pk = post.pk)
    else:
        form = PostForm()
    return render(request, 'yblog/post_add.html',{'form': form})
"""

####
@login_required
def post_new(request):
    if request.method=='POST':
        post_form = PostForm(request.POST)
        image_formset = ImageFormSet(request.POST, request.FILES)
        if post_form.is_valid() and image_formset.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            
            #post.save()
            with transaction.atomic():
                post.save()
                image_formset.instance = post
                image_formset.save()
                return redirect("post_detail", pk=post.pk)
    else:
        post_form = PostForm()
        image_formset = ImageFormSet()
    return render(request, 'yblog/post_add.html',{'post_form':post_form, 'image_formset':image_formset})
####

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'yblog/post_detail.html',{'post':post})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'yblog/post_add.html',{'post_form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('/')

@login_required
def post_search(request):
    results = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        results = Post.objects.all().filter(Q(title__icontains=query)|Q(text__icontains=query))
        ####
        paginator = Paginator(results, 12)
        page_number = request.GET.get('page')
        search_obj = paginator.get_page(page_number)
        ####
    return render(request, 'yblog/search_results.html', {'query':query, 'results':search_obj})

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'yblog/add_comments.html',{'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def study_post(request):
    studies = Post.objects.filter(category__iexact=1).order_by('-published_date')
    paginator = Paginator(studies, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'yblog/study.html',{'studies':page_obj}) #send the study post queries to study page

@login_required
def clubs_post(request):
    clubs = Post.objects.filter(category__iexact=2).order_by('-published_date')
    paginator = Paginator(clubs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'yblog/clubs.html',{'clubs':page_obj})

@login_required
def notice_post(request):
    notices = Post.objects.filter(category__iexact=3).order_by('-published_date')
    paginator = Paginator(notices, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'yblog/notice.html',{'notices':page_obj})

@login_required
def social_post(request):
    socials = Post.objects.filter(category__iexact=4).order_by('-published_date')
    paginator = Paginator(socials, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'yblog/social.html',{'socials':page_obj})

@login_required
def post_preference(request, pk, userpreference):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        obj = ''
        valueobj = ''
        try:
            obj = Preference.objects.get(user=request.user, post = post)
            valueobj = obj.value
            valueobj = int(valueobj)
            userpreference = int(userpreference) #userpreference from the post_detail page
            if valueobj != userpreference:
                obj.delete()
                upref = Preference()
                upref.user = request.user
                upref.post = post
                upref.value = userpreference
                if userpreference == 1 and valueobj != 1:
                    post.likes +=1
                    post.dislikes -=1
                elif userpreference == 2 and valueobj !=2:
                    post.dislikes +=1
                    post.likes -=1
                upref.save()
                post.save()
                context = {'post':post,
                    'pk':pk}
                return redirect('post_detail', pk=post.pk)

            elif valueobj == userpreference:
                obj.delete()

                if userpreference == 1:
                    post.likes -= 1
                elif userpreference == 2:
                    post.dislikes -= 1
                
                post.save()

                context = {'post':post,
                    'pk':pk}
                return redirect('post_detail', pk=post.pk)

        except Preference.DoesNotExist:
            upref = Preference()
            upref.user = request.user
            upref.post = post
            upref.value = userpreference
            userpreference = int(userpreference)
            if userpreference == 1:
                post.likes +=1
            elif userpreference == 2:
                post.dislikes += 1
            upref.save()
            post.save()

            context={'post':post,
                'pk':pk}
            return redirect('post_detail', pk=post.pk)

def my_page(request):
    user = request.user
    posts = Post.objects.filter(author__iexact = request.user)
    study_posts = posts.filter(category__iexact = 1).order_by('-published_date')
    club_posts = posts.filter(category__iexact = 2).order_by('-published_date')
    notice_posts = posts.filter(category__iexact = 3).order_by('-published_date')
    social_posts = posts.filter(category__iexact = 4).order_by('-published_date')
    my_posts={'user':user, 'stposts':study_posts, 'clposts':club_posts, 'noposts':notice_posts,'soposts':social_posts}
    return render(request, 'yblog/my_page.html', my_posts)