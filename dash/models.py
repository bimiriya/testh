from django.db import models
import os
from django.shortcuts import get_object_or_404
# Create your models here.

class Post(models.Model):
    img = models.FileField(upload_to='upload')
    base_64 = models.TextField(null=True,blank=True)
    nickname = models.CharField(max_length=100)
    pet_name = models.CharField(max_length=100)
    votes_up = models.IntegerField(default=0)
    votes_down = models.IntegerField(default=0)
    total_votes = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-total_votes']

    def __str__(self):
        return self.nickname
    
    @staticmethod
    def create(request):
        form = request.POST
        new = Post()
        new.img = request.FILES['img']
        new.nickname = request.POST.get('nickname')
        new.pet_name = request.POST.get('pet_name')
        new.save()
        new.base64()
    
    def base64(self):
        import base64
        img = self.img.file
        encoded_string = ''
        with open(self.img.path, "rb") as img_f:
            encoded_string = base64.b64encode(img_f.read())
            decoded = encoded_string.decode("utf-8")
            base64 = 'data:image/%s;base64,%s' % ('jpg', decoded)
            self.base_64 = base64
            self.save()

    @staticmethod
    def get_all():
        posts = Post.objects.all()
        return list(posts.values())
    
    @staticmethod
    def get_by(pk=None):
        if pk is not None:
            post = get_object_or_404(Post,pk=pk)
            return post
    @staticmethod
    def vote(request):
        pk = request.POST.get('pk')
        post = Post.get_by(pk=pk)
        
        which = request.POST.get('bool')
        if which == 'true':
            post.votes_up += 1
        elif which == 'false':
            post.votes_down += 1
        post.save()

        post.calc_total()
    
    def calc_total(self):
        self.total_votes = self.votes_up + self.votes_down
        self.save()
        
