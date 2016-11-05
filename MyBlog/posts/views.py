from urllib import parse
from django.shortcuts import render, get_object_or_404, Http404,  redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .forms import PostForm, CommentForm, UserLoginForm, UserSigninForm
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def comment_create(request, slug):
    if(request.user.is_authenticated()):
        form = CommentForm(request.POST or None)
        if(form.is_valid()):
            instance = form.save(commit=False)
            instance.user = request.user
            instance.post = get_object_or_404(Post, slug = slug)
            in_post = instance.post
            instance.save()
            messages.success(request, "Successfully created")
            return HttpResponseRedirect(in_post.get_absolute_url())
        #else:
        #    messages.error(request, "Failed to create")
        context = {
            "form": form,
        }
        return render(request, "comment_form.html", context)
    raise Http404
def post_detail(request, slug):
    if(slug != "about"):
        instance = get_object_or_404(Post, slug = slug)
        share_string = parse.quote(instance.content)
        tags = instance.tag_list.split
        context = {
            "title": instance.title,
            "instance": instance,
            "share_string": share_string,
            "tags": tags
        }
        return render(request, "post_detail.html", context)
    else:
        return redirect("posts:about_page")
    raise Http404
def about_page(request):
    instance = get_object_or_404(Post, slug = "about")
    share_string = parse.quote(instance.content)
    tags = instance.tag_list.split
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "tags": tags
    }
    return render(request, "about-MyBlog.html", context)
def post_update(request, slug = None):
    if request.user.is_staff or request.user.is_superuser:
        instance = get_object_or_404(Post, slug = slug)
        form = PostForm(request.POST or None, request.FILES or None, instance = instance)
        if(form.is_valid()):
            instance = form.save(commit=False)
            instance.tag_list = instance.tag_list+" "
            instance.save()
            messages.success(request, "Successfully updated")
            return HttpResponseRedirect(instance.get_absolute_url())
        context = {
            "title": instance.title,
            "instance": instance,
            "form": form,
        }
        return render(request, "post_form.html", context)
    else:
         raise Http404
def comment_update(request, slug, id):
    if request.user.is_authenticated():
        instance = get_object_or_404(Comment, id = id)
        form = CommentForm(request.POST or None, instance = instance)
        if(form.is_valid()):
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Successfully updated")
            instance = get_object_or_404(Post, slug = slug)
            return HttpResponseRedirect(instance.get_absolute_url())
        context = {
            "instance": instance,
            "form": form,
        }
        return render(request, "comment_form.html", context)
    else:
        raise Http404
def comment_delete(request, slug, id):
    if request.user.is_authenticated():
        instance = get_object_or_404(Comment, id = id)
        instance.delete()
        messages.success(request, "Successfully deleted")
        instance = get_object_or_404(Post, slug = slug)
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        raise Http404
def post_list(request):
    queryset_list = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(queryset_list, 10)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        "object_list" : queryset,
        "title": "List",
        "page_request_var": page_request_var
    }    
    return render(request, "post_list.html", context)
def search_tag(request, tag):
    queryset_list = Post.objects.filter(tag_list__contains= "#"+tag+ " ").order_by("-timestamp")
    paginator = Paginator(queryset_list, 10)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        "object_list" : queryset,
        "title": "List",
        "page_request_var": page_request_var
    }    
    return render(request, "post_list.html", context)
def post_delete(request, slug):
    if request.user.is_staff or request.user.is_superuser:
        instance = get_object_or_404(Post, slug = slug)
        instance.delete()
        messages.success(request, "Successfully deleted")
        return redirect("posts:list")
    else:
        raise Http404
def post_create(request):
    if(request.user.is_staff or request.user.is_superuser):
        form = PostForm(request.POST or None, request.FILES or None)
        if(form.is_valid()):
            instance = form.save(commit=False)
            instance.user = request.user
            instance.tag_list = instance.tag_list+" "
            instance.save()
            messages.success(request, "Successfully created")
            return HttpResponseRedirect(instance.get_absolute_url())
        #else:
        #    messages.error(request, "Failed to create")
        context = {
            "form": form,
        }
        return render(request, "post_form.html", context)
    raise Http404
def signin_user(request):
    form = UserSigninForm(request.POST or None)
    if(form.is_valid()):
        instance = form.save(commit=False)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        instance.set_password(password)
        instance.save()
        instance = authenticate(username = username, password = password)
        if instance is not None:
            login(request, instance)
            messages.success(request, "Welcome, " + username)
            return redirect("posts:list")
    context = {
            "form": form,
    }
    return render(request, "user_form.html", context)
def login_user(request):
    form = UserLoginForm(request.POST or None)
    if(form.is_valid()):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username = username, password = password)
        login(request, user)
        messages.success(request, "Welcome, " + username)
        return redirect("posts:list")
    context = {
            "form": form,
    }
    return render(request, "user_form.html", context)
def logout_user(request):
    logout(request)
    return redirect("posts:list")