from django.contrib import admin
from django.urls import path
from .views import main,get_posts,vote

urlpatterns = [
    path('', main,name='main'),
    path('get_posts/', get_posts, name="get_posts"),
    path('vote/', vote, name="vote")
] 
