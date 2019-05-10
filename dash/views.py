from django.shortcuts import render
from django.views.generic import View
from .forms import PostForm
from .models import Post
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.views.generic import View,FormView
from django.urls import reverse_lazy , reverse

def main(request):
    form = PostForm()
    context = {
        'form': form
    }
    if request.method == 'GET':
        return render(request, 'dash/main.html', context)
    if request.method == 'POST':
        Post.create(request)
        return render(request, 'dash/main.html', context)
        


def get_posts(request):
    posts = Post.get_all()
    response = {
        'posts': posts
    }
    return JsonResponse(response, safe=False)

def vote(request):
    if request.method == 'POST':
        Post.vote(request)
        return HttpResponse(status=204)