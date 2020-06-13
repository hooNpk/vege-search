from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=30)
    location = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=30, null=True)

    def __str__(self):
        return '{}::{}'.format(self.restaurant_name, self.location)

class Post(models.Model):
    title = models.CharField(max_length=30)  # 블로그 글 제목
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    #restaurant = models.CharField(max_length=30, default=True)

    meat = models.BooleanField(default=True)
    fish = models.BooleanField(default=True)
    egg = models.BooleanField(default=True)
    milk = models.BooleanField(default=True)
    content = models.TextField()  # 블로그 내용

    head_image = models.ImageField(upload_to='blog/%Y/%m/%d/', blank=True)
    created = models.DateTimeField(auto_now_add=True)  # 작성 일시
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 어떤 유저가 썼는지.

    def __str__(self):
        return '{}::{}'.format(self.title, self.author)

    def get_update_url(self):
        return self.get_absolute_url() + 'update/'

    def get_absolute_url(self):
        return '/blog/{}/'.format(self.pk)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    taste = models.IntegerField(null=True)
    trust = models.IntegerField(null=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return self.post.get_absolute_url() + '#comment-id-{}'.format(self.pk)